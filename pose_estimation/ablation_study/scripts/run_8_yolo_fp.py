import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import sys, json, time
import numpy as np
import trimesh
import cv2
from pathlib import Path
from PIL import Image
import nvdiffrast.torch as dr
from ultralytics import YOLO

_script_dir = Path(__file__).resolve().parent
_candidates = [
    Path("/home/salman/rai_workspace/ablation_study"),
    _script_dir.parent,
    _script_dir.parent.parent,
]
PROJECT_ROOT = next((p for p in _candidates if (p / "megapose_objects").exists()), _candidates[0])
sys.path.insert(0, str(_script_dir))
from objects_config_v2 import (
    OBJECTS, gt_pose_to_matrix, rotation_error_deg, position_error_cm,
    add_score, cluster_estimates, depth_mask_from_bbox,
    save_det_viz, save_pose_viz,
)

FP_ROOT = Path.home() / "rai_workspace/FoundationPose"
sys.path.insert(0, str(FP_ROOT))
sys.path.insert(0, str(FP_ROOT / "mycuda"))

YOLO_WEIGHTS   = PROJECT_ROOT / "yolo_dataset/models/yolov8_objects/weights/best.pt"
CAM_INFO       = PROJECT_ROOT / "outputs/camera_info.json"
ENV_NAME       = "env_80"
OUT_DIR        = PROJECT_ROOT / "outputs/ablation_v2"
VIS_DIR        = OUT_DIR / "vis" / "yolo_fp"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

YOLO_CONF      = 0.001   # near-zero: accept any detection the model fires
YOLO_IOU       = 0.45
MAX_PER_CAMERA = 2
MAX_TOTAL      = 8
N_FP_ITER      = 5
DEPTH_TOL      = 0.15
DEVICE         = "cuda"

print(f"Loading YOLOv8 from {YOLO_WEIGHTS} …")
assert YOLO_WEIGHTS.exists(), f"Weights not found: {YOLO_WEIGHTS}"
yolo = YOLO(str(YOLO_WEIGHTS))
yolo.to(DEVICE)
print(f"YOLO classes: {list(yolo.names.values())}")

print("Loading FoundationPose scorer + refiner …")
from estimater import FoundationPose, PoseRefinePredictor, ScorePredictor
scorer  = ScorePredictor()
refiner = PoseRefinePredictor()
glctx   = dr.RasterizeCudaContext()

from env_utils import load_camera_info_for_env
camera_info = load_camera_info_for_env(CAM_INFO, ENV_NAME, PROJECT_ROOT)
camera_info = {k: v for k, v in camera_info.items() if k == "cam_dim_0"}

results = {}

for label, cfg in OBJECTS.items():
    print(f"\n{'='*60}\nObject: {label}  yolo_class: {cfg['yolo_class']}\n{'='*60}")
    T_gt    = gt_pose_to_matrix(cfg["gt_pose"])
    result  = {"status": "no_detection"}
    vis_dir = VIS_DIR / label
    vis_dir.mkdir(parents=True, exist_ok=True)

    yolo_cls_name = cfg.get("yolo_class")
    if yolo_cls_name is None:
        print(f"  '{label}' has no matching YOLO class — skipping")
        results[label] = {"status": "class_not_in_model"}
        continue

    cls_id = next((cid for cid, n in yolo.names.items() if n == yolo_cls_name), None)
    if cls_id is None:
        print(f"  Class '{yolo_cls_name}' not found in YOLO model — skipping")
        results[label] = {"status": "class_not_in_model"}
        continue

    print(f"  YOLO class id: {cls_id}  ('{yolo_cls_name}')  conf threshold: {YOLO_CONF}")

    t0_det   = time.perf_counter()
    all_dets = []

    for cam_name, info in camera_info.items():
        rgb_bgr = cv2.imread(info["rgb_path"])
        depth   = np.load(info["depth_path"]).astype(np.float32)
        res     = yolo.predict(source=str(info["rgb_path"]), conf=YOLO_CONF, iou=YOLO_IOU,
                               classes=[cls_id], verbose=False)[0]
        boxes   = res.boxes
        if boxes is None or len(boxes) == 0:
            print(f"  {cam_name}: no detection even at conf={YOLO_CONF}")
            continue

        scores = boxes.conf.cpu().numpy()
        xyxy   = boxes.xyxy.cpu().numpy()
        order  = np.argsort(scores)[::-1][:MAX_PER_CAMERA]

        for i in order:
            score = float(scores[i])
            box   = xyxy[i]
            print(f"  {cam_name}: conf={score:.4f}  box={box.astype(int).tolist()}")
            mask  = depth_mask_from_bbox(depth, box, tol=DEPTH_TOL)
            all_dets.append({
                "score":    score,
                "cam":      cam_name,
                "box_xyxy": box,
                "mask":     mask,
                "info":     info,
            })

    det_time = time.perf_counter() - t0_det

    if not all_dets:
        print("  No detections — skipping")
        results[label] = {"status": "no_detection"}
        continue

    all_dets.sort(key=lambda d: d["score"], reverse=True)
    top_dets = all_dets[:MAX_TOTAL]
    print(f"  {len(top_dets)} detection(s) in {det_time:.2f}s")

    for di, det in enumerate(top_dets):
        rgb_bgr = cv2.imread(det["info"]["rgb_path"])
        save_det_viz(
            vis_dir / f"det_{di:02d}_{det['cam']}.png",
            rgb_bgr, det["box_xyxy"], det["score"], det["cam"],
            mask=det["mask"], color=(0, 255, 150),
            extra_text=f"[YOLO cls={yolo_cls_name} conf={det['score']:.4f}, depth mask]",
        )
    print(f"  Det viz → {vis_dir}")

    mesh_path = PROJECT_ROOT / "megapose_objects" / label / "mesh.ply"
    mesh      = trimesh.load(str(mesh_path))
    fp_est    = FoundationPose(
        model_pts     = np.array(mesh.vertices,       dtype=np.float32),
        model_normals = np.array(mesh.vertex_normals,  dtype=np.float32),
        mesh          = mesh,
        scorer        = scorer,
        refiner       = refiner,
        debug_dir     = "/tmp/fp_debug",
        debug         = 0,
        glctx         = glctx,
    )
    verts_hom = np.hstack([np.array(mesh.vertices),
                            np.ones((len(mesh.vertices), 1))])

    t0_est    = time.perf_counter()
    estimates = []

    for det in top_dets:
        info  = det["info"]
        rgb   = np.array(Image.open(info["rgb_path"]).convert("RGB"))
        depth = np.load(info["depth_path"]).astype(np.float32)
        K     = np.array(info["K"],           dtype=np.float64)
        T_wc  = np.array(info["T_world_cam"], dtype=np.float64)

        try:
            T_co = fp_est.register(
                K=K, rgb=rgb, depth=depth,
                ob_mask=det["mask"], iteration=N_FP_ITER,
            )
        except Exception as e:
            print(f"    FP failed: {e}")
            continue

        T_wo = T_wc @ T_co
        try:
            save_pose_viz(
                vis_dir / f"pose_{len(estimates):02d}_{det['cam']}.png",
                cv2.imread(info["rgb_path"]), K, T_co, T_wo, verts_hom,
                color=(0, 255, 150),
            )
        except Exception as ve:
            print(f"    Pose viz failed: {ve}")

        estimates.append({
            "position": T_wo[:3, 3],
            "score":    det["score"],
            "T_wo":     T_wo,
        })

    est_time = time.perf_counter() - t0_est

    if not estimates:
        print("  No pose estimates produced")
        result["status"] = "estimation_failed"
        results[label]   = result
        continue

    clusters = cluster_estimates(estimates)
    T_est    = clusters[0]["rep"]["T_wo"]
    pos_err  = position_error_cm(T_est[:3, 3], T_gt[:3, 3])
    rot_err  = rotation_error_deg(T_est[:3, :3], T_gt[:3, :3])
    add_cm, diam_cm, add_ok = add_score(np.array(mesh.vertices), T_est, T_gt)

    print(f"  Position error : {pos_err:.1f} cm")
    print(f"  Rotation error : {rot_err:.1f} deg")
    print(f"  ADD            : {add_cm:.3f} cm  (diam={diam_cm:.2f} cm)  {'✓' if add_ok else '✗'}")
    print(f"  Time           : det={det_time:.2f}s  est={est_time:.2f}s")

    results[label] = {
        "status":             "success",
        "yolo_class":         yolo_cls_name,
        "yolo_conf_used":     round(float(top_dets[0]["score"]), 6),
        "position_error_cm":  round(pos_err, 3),
        "rotation_error_deg": round(rot_err, 3),
        "add_cm":             round(add_cm, 4),
        "add_diameter_cm":    round(diam_cm, 4),
        "add_success":        bool(add_ok),
        "detection_time_s":   round(det_time, 3),
        "estimation_time_s":  round(est_time, 3),
        "total_time_s":       round(det_time + est_time, 3),
        "n_detections_used":  len(estimates),
        "T_est":              T_est.tolist(),
        "T_gt":               T_gt.tolist(),
    }

out_path = OUT_DIR / "results_yolo_fp.json"
with open(out_path, "w") as f:
    json.dump({"method": "yolo_fp", "results": results}, f, indent=2)
print(f"\nSaved → {out_path}")
