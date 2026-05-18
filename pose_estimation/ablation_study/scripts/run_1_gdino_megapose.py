import os, sys, json, time
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
import torch
import pandas as pd
import trimesh
import cv2
from pathlib import Path
from PIL import Image

_HP_DATA = Path.home() / "rai_workspace" / "happypose_data"
if "HAPPYPOSE_DATA_DIR" not in os.environ or not Path(os.environ["HAPPYPOSE_DATA_DIR"]).exists():
    os.environ["HAPPYPOSE_DATA_DIR"] = str(_HP_DATA)

_script_dir = Path(".").resolve().parent
_candidates = [
    Path("/home/salman/rai_workspace/ablation_study"),
    _script_dir.parent,
    _script_dir.parent.parent,
]

PROJECT_ROOT = next((p for p in _candidates if (p / "megapose_objects").exists()), _candidates[0])

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from objects_config_v2 import (
    OBJECTS, gt_pose_to_matrix, rotation_error_deg, position_error_cm,
    add_score, cluster_estimates, boxes_cxcywh_to_xyxy,
    save_det_viz, save_pose_viz,
)

GD_CONFIG  = Path.home() / "rai_workspace/grounding_dino_weights/GroundingDINO_SwinT_OGC.py"
GD_WEIGHTS = Path.home() / "rai_workspace/grounding_dino_weights/groundingdino_swint_ogc.pth"
CAM_INFO   = PROJECT_ROOT / "outputs/camera_info.json"
ENV_NAME   = "env_80"   # set to None to use default outputs/rgb images
OUT_DIR    = PROJECT_ROOT / "outputs/ablation_v2"
VIS_DIR    = OUT_DIR / "vis" / "gdino_megapose"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

BOX_THRESHOLD  = 0.25
TEXT_THRESHOLD = 0.20
MAX_PER_CAMERA = 2
MAX_TOTAL      = 8
N_REFINER_ITER = 5
DEVICE         = "cuda"

print("Loading GroundingDINO …")
from groundingdino.util.inference import load_model, load_image, predict
gd_model = load_model(str(GD_CONFIG), str(GD_WEIGHTS))
gd_model.eval()

print("Loading MegaPose …")
from happypose.toolbox.datasets.object_dataset import RigidObjectDataset, RigidObject
from happypose.toolbox.utils.load_model import load_named_model
from happypose.toolbox.inference.types import ObservationTensor
from happypose.toolbox.utils.tensor_collection import PandasTensorCollection

object_dataset = RigidObjectDataset([
    RigidObject(
        label=label,
        mesh_path=PROJECT_ROOT / "megapose_objects" / label / "mesh.ply",
        scaling_factor=1.0,
    )
    for label in OBJECTS
])
pose_estimator = load_named_model("megapose-1.0-RGBD", object_dataset=object_dataset)
pose_estimator._SO3_grid = pose_estimator._SO3_grid.to(DEVICE)

from env_utils import load_camera_info_for_env
camera_info = load_camera_info_for_env(CAM_INFO, ENV_NAME, PROJECT_ROOT)

results = {}

for label, cfg in OBJECTS.items():
    print(f"\n{'='*60}\nObject: {label}  prompt: '{cfg['prompt']}'\n{'='*60}")
    T_gt   = gt_pose_to_matrix(cfg["gt_pose"])
    result = {"status": "no_detection"}
    vis_dir = VIS_DIR / label
    vis_dir.mkdir(parents=True, exist_ok=True)

    t0_det   = time.perf_counter()
    all_dets = []

    for cam_name, info in camera_info.items():
        W, H = info["width"], info["height"]
        _, img_tensor = load_image(info["rgb_path"])
        boxes_norm, logits, _ = predict(
            model=gd_model, image=img_tensor, caption=cfg["prompt"],
            box_threshold=BOX_THRESHOLD, text_threshold=TEXT_THRESHOLD,
        )
        if len(logits) == 0:
            continue
        boxes_xyxy = boxes_cxcywh_to_xyxy(boxes_norm, W, H)
        order = logits.argsort(descending=True)[:MAX_PER_CAMERA]
        for i in order:
            all_dets.append({
                "score":    logits[i].item(),
                "cam":      cam_name,
                "box_xyxy": boxes_xyxy[i].numpy(),
                "info":     info,
            })

    det_time = time.perf_counter() - t0_det

    if not all_dets:
        print("  No detections — skipping")
        results[label] = result
        continue

    all_dets.sort(key=lambda d: d["score"], reverse=True)
    top_dets = all_dets[:MAX_TOTAL]
    print(f"  {len(top_dets)} detection(s) in {det_time:.2f}s")

    for di, det in enumerate(top_dets):
        rgb_bgr = cv2.imread(det["info"]["rgb_path"])
        save_det_viz(
            vis_dir / f"det_{di:02d}_{det['cam']}.png",
            rgb_bgr, det["box_xyxy"], det["score"], det["cam"],
            color=(0, 200, 0),
        )
    print(f"  Det viz → {vis_dir}")

    mesh_path = PROJECT_ROOT / "megapose_objects" / label / "mesh.ply"
    mesh      = trimesh.load(str(mesh_path))
    verts_hom = np.hstack([np.array(mesh.vertices),
                            np.ones((len(mesh.vertices), 1))])

    t0_est    = time.perf_counter()
    estimates = []

    for det in top_dets:
        info  = det["info"]
        rgb   = np.array(Image.open(info["rgb_path"]).convert("RGB"))
        depth = np.load(info["depth_path"])
        K     = np.array(info["K"], dtype=np.float64)
        T_wc  = np.array(info["T_world_cam"])
        box   = torch.tensor(det["box_xyxy"]).unsqueeze(0).float().to(DEVICE)
        obs   = ObservationTensor.from_numpy(rgb=rgb, depth=depth, K=K).to(DEVICE)
        tc    = PandasTensorCollection(
            infos=pd.DataFrame({
                "label": [label], "batch_im_id": [0],
                "instance_id": [0], "score": [float(det["score"])],
            }),
            bboxes=box,
        )
        try:
            out, _ = pose_estimator.run_inference_pipeline(
                obs, detections=tc, run_detector=False,
                n_refiner_iterations=N_REFINER_ITER, n_pose_hypotheses=1,
            )
        except Exception as e:
            print(f"    MegaPose failed: {e}")
            continue

        T_co = out.poses[0].cpu().numpy()
        T_wo = T_wc @ T_co

        try:
            save_pose_viz(
                vis_dir / f"pose_{len(estimates):02d}_{det['cam']}.png",
                cv2.imread(info["rgb_path"]), K, T_co, T_wo, verts_hom,
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

out_path = OUT_DIR / "results_gdino_megapose.json"
with open(out_path, "w") as f:
    json.dump({"method": "gdino_megapose", "results": results}, f, indent=2)
print(f"\nSaved → {out_path}")
