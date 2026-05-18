import argparse
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(".").resolve().parent

DEFAULT_CKPT = (PROJECT_ROOT / "yolo_dataset" / "models"
                / "yolov8_objects" / "weights" / "best.pt")
DATASET_YAML = PROJECT_ROOT / "yolo_dataset" / "dataset.yaml"

parser = argparse.ArgumentParser()
parser.add_argument("--weights", default=str(DEFAULT_CKPT))
parser.add_argument("--image",   default=None,
                    help="Single image path for visualised inference (optional)")
parser.add_argument("--conf",    type=float, default=0.25)
parser.add_argument("--iou",     type=float, default=0.45)
parser.add_argument("--imgsz",   type=int,   default=640)
parser.add_argument("--device",  default="0")
args = parser.parse_args()

ckpt = Path(args.weights)
assert ckpt.exists(), f"Weights not found: {ckpt}"

print(f"Weights : {ckpt}")
print(f"Conf    : {args.conf}  |  IoU: {args.iou}\n")
model = YOLO(str(ckpt))

if args.image is None:
    assert DATASET_YAML.exists(), f"Dataset YAML not found: {DATASET_YAML}"

    metrics = model.val(
        data    = str(DATASET_YAML),
        split   = "val",
        conf    = args.conf,
        iou     = args.iou,
        imgsz   = args.imgsz,
        device  = args.device,
        verbose = True,
    )

    print("\n── Validation Metrics ───────────────────────────────────────────────────")
    print(f"  mAP@0.5       : {metrics.box.map50:.4f}")
    print(f"  mAP@0.5:0.95  : {metrics.box.map:.4f}")
    print(f"  Precision     : {metrics.box.mp:.4f}")
    print(f"  Recall        : {metrics.box.mr:.4f}")

    print("\n── Per-class AP@0.5 ─────────────────────────────────────────────────────")
    for cls_name, ap in zip(metrics.names.values(), metrics.box.ap50):
        print(f"  {cls_name:<22s}  {ap:.4f}")

else:
    img_path = Path(args.image)
    assert img_path.exists(), f"Image not found: {img_path}"

    results = model.predict(
        source  = str(img_path),
        conf    = args.conf,
        iou     = args.iou,
        imgsz   = args.imgsz,
        device  = args.device,
        verbose = False,
    )[0]

    img = cv2.imread(str(img_path))
    boxes = results.boxes

    if boxes is None or len(boxes) == 0:
        print("No detections.")
    else:
        PALETTE = [
            (0, 255, 0), (0, 165, 255), (255, 0, 255),
            (255, 255, 0), (0, 0, 255), (255, 128, 0),
        ]
        for i, (xyxy, conf, cls_id) in enumerate(
            zip(boxes.xyxy.cpu().numpy(),
                boxes.conf.cpu().numpy(),
                boxes.cls.cpu().numpy().astype(int))
        ):
            x1, y1, x2, y2 = xyxy.astype(int)
            color    = PALETTE[i % len(PALETTE)]
            cls_name = model.names[cls_id]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            cv2.putText(img, f"{cls_name} {conf:.2f}",
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            print(f"  [{i+1}] {cls_name:22s}  conf={conf:.3f}  box={[x1,y1,x2,y2]}")

    out_path = img_path.parent / f"{img_path.stem}_yolo_det{img_path.suffix}"
    cv2.imwrite(str(out_path), img)
    print(f"\nSaved visualisation → {out_path}")
