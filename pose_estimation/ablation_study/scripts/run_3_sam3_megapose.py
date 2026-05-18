import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import gc, sys, json, time, tempfile
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
    add_score, cluster_estimates, boxes_cxcywh_to_xyxy, mask_to_bbox,
    save_det_viz, save_pose_viz,
)

GD_CONFIG  = Path.home() / "rai_workspace/grounding_dino_weights/GroundingDINO_SwinT_OGC.py"
GD_WEIGHTS = Path.home() / "rai_workspace/grounding_dino_weights/groundingdino_swint_ogc.pth"
CAM_INFO   = PROJECT_ROOT / "outputs/camera_info.json"
ENV_NAME   = "env_80"
OUT_DIR    = PROJECT_ROOT / "outputs/ablation_v2"
VIS_DIR    = OUT_DIR / "vis" / "sam3_megapose"
OUT_DIR.mkdir(parents=True, exist_ok=True)
VIS_DIR.mkdir(parents=True, exist_ok=True)

GD_BOX_THRESHOLD  = 0.25
GD_TEXT_THRESHOLD = 0.20
SAM3_MASK_THRESH  = 0.50
MAX_PER_CAMERA    = 2
MAX_TOTAL         = 4 
N_REFINER_ITER    = 5
DEVICE            = "cuda"

from env_utils import load_camera_info_for_env
camera_info = load_camera_info_for_env(CAM_INFO, ENV_NAME, PROJECT_ROOT)

print("\n" + "="*60)
print("PHASE 1: Loading GD + SAM3 for detection across all objects")
print("="*60)

from groundingdino.util.inference import load_model, load_image, predict
gd_model = load_model(str(GD_CONFIG), str(GD_WEIGHTS))
gd_model.eval()

from transformers import Sam3Processor, Sam3Model
sam3_processor = Sam3Processor.from_pretrained("facebook/sam3")
sam3_model     = Sam3Model.from_pretrained("facebook/sam3").to(DEVICE)
sam3_model.eval()

all_detections = {}
det_times      = {}

for label, cfg in OBJECTS.items():
    print(f"\n  Detecting: {label}  ('{cfg['prompt']}')")
    vis_dir = VIS_DIR / label
    vis_dir.mkdir(parents=True, exist_ok=True)

    t0_det   = time.perf_counter()
    all_dets = []

    for cam_name, info in camera_info.items():
        W, H      = info["width"], info["height"]
        image_pil = Image.open(info["rgb_path"]).convert("RGB")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        image_pil.save(tmp_path)
        try:
            _, img_tensor = load_image(tmp_path)
            boxes_norm, logits, _ = predict(
                model=gd_model, image=img_tensor, caption=cfg["prompt"],
                box_threshold=GD_BOX_THRESHOLD, text_threshold=GD_TEXT_THRESHOLD,
            )
        finally:
            os.unlink(tmp_path)

        if len(logits) == 0:
            continue

        boxes_xyxy = boxes_cxcywh_to_xyxy(boxes_norm, W, H)
        order      = logits.argsort(descending=True)[:MAX_PER_CAMERA]
        rgb_bgr    = cv2.imread(info["rgb_path"])

        for i in order:
            score  = logits[i].item()
            gd_box = boxes_xyxy[i].numpy()

            inputs = sam3_processor(
                images=image_pil,
                input_boxes=[[gd_box.tolist()]],
                input_boxes_labels=[[1]],
                return_tensors="pt",
            ).to(DEVICE)
            with torch.no_grad():
                outputs = sam3_model(**inputs)
            res = sam3_processor.post_process_instance_segmentation(
                outputs, threshold=0.0, mask_threshold=SAM3_MASK_THRESH,
                target_sizes=inputs.get("original_sizes").tolist(),
            )[0]
            if len(res["masks"]) == 0:
                continue
            mask = res["masks"][0].cpu().numpy().astype(bool)
            if not mask.any():
                continue

            tight_box = mask_to_bbox(mask)
            if tight_box is None:
                continue

            det_idx = len(all_dets)
            save_det_viz(
                vis_dir / f"det_{det_idx:02d}_{cam_name}.png",
                rgb_bgr, gd_box, score, cam_name,
                mask=mask, color=(255, 80, 0),
                extra_text="[SAM3 mask shown]",
            )
            del mask

            all_dets.append({
                "score":    score,
                "cam":      cam_name,
                "box_xyxy": tight_box,
                "gd_box":   gd_box,
                "info":     info,
            })

    det_time = time.perf_counter() - t0_det
    all_dets.sort(key=lambda d: d["score"], reverse=True)
    top_dets = all_dets[:MAX_TOTAL]

    all_detections[label] = top_dets
    det_times[label]      = det_time
    print(f"    {len(top_dets)} detection(s) in {det_time:.2f}s  → viz: {vis_dir}")

print("\nFreeing GD + SAM3 from GPU …")
del gd_model, sam3_model, sam3_processor
gc.collect()
torch.cuda.empty_cache()


print("\n" + "="*60)
print("PHASE 2: Loading MegaPose for pose estimation")
print("="*60)

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

results = {}

for label, cfg in OBJECTS.items():
    print(f"\n{'='*60}\nObject: {label}\n{'='*60}")
    T_gt     = gt_pose_to_matrix(cfg["gt_pose"])
    vis_dir  = VIS_DIR / label
    top_dets = all_detections[label]
    det_time = det_times[label]

    if not top_dets:
        print("  No detections — skipping")
        results[label] = {"status": "no_detection"}
        continue

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
                color=(255, 80, 0),
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
        results[label] = {"status": "estimation_failed"}
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

out_path = OUT_DIR / "results_sam3_megapose.json"
with open(out_path, "w") as f:
    json.dump({"method": "sam3_megapose", "results": results}, f, indent=2)
print(f"\nSaved → {out_path}")
