import argparse
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(".").resolve().parent

DATASET_YAML = PROJECT_ROOT / "yolo_dataset" / "dataset.yaml"
MODELS_DIR   = PROJECT_ROOT / "yolo_dataset" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--model",   default="yolov8m.pt",
                    help="Base model weights (downloads automatically if not cached)")
parser.add_argument("--epochs",  type=int,   default=100)
parser.add_argument("--imgsz",   type=int,   default=640)
parser.add_argument("--batch",   type=int,   default=16)
parser.add_argument("--workers", type=int,   default=4)
parser.add_argument("--device",  default="0",
                    help="GPU id(s), e.g. '0' or '0,1', or 'cpu'")
args = parser.parse_args()

assert DATASET_YAML.exists(), (
    f"Dataset YAML not found: {DATASET_YAML}\n"
    "Run scripts/yolo_pipeline/render_dataset.py first."
)

print(f"Dataset : {DATASET_YAML}")
print(f"Base    : {args.model}")
print(f"Epochs  : {args.epochs}  |  imgsz={args.imgsz}  |  batch={args.batch}")
print(f"Device  : {args.device}\n")

model = YOLO(args.model)

results = model.train(
    data     = str(DATASET_YAML),
    epochs   = args.epochs,
    imgsz    = args.imgsz,
    batch    = args.batch,
    workers  = args.workers,
    device   = args.device,
    project  = str(MODELS_DIR),
    name     = "yolov8_objects",
    exist_ok = True,
    
    flipud   = 0.3,
    fliplr   = 0.5,
    hsv_h    = 0.02,
    hsv_s    = 0.5,
    hsv_v    = 0.3,
    degrees  = 15,
    scale    = 0.3,
    mosaic   = 0.5,
)

best_ckpt = MODELS_DIR / "yolov8_objects" / "weights" / "best.pt"
print(f"\nTraining complete.")
print(f"  Best weights → {best_ckpt}")
print(f"  mAP@0.5      : {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
