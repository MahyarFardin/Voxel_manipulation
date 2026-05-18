import argparse
import random
import cv2
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(".").resolve().parent

DATASET_DIR  = PROJECT_ROOT / "yolo_dataset"
OUT_DIR      = DATASET_DIR / "annotation_check"

CLASS_NAMES = [
    "airplane", "bed", "car", "chair", "cone",
    "firefighterFigure", "guitar", "lamp", "laptop",
    "monitor", "piano", "stairs", "table", "vase", "xbox",
]
PALETTE = [
    (0,255,0),(0,165,255),(255,0,255),(255,255,0),(0,0,255),
    (255,128,0),(128,0,255),(0,255,255),(255,0,128),(128,255,0),
    (0,128,255),(255,128,128),(128,128,0),(0,128,128),(128,0,128),
]

parser = argparse.ArgumentParser()
parser.add_argument("--split",  default="train", choices=["train","val","both"])
parser.add_argument("--n",      type=int, default=20, help="Images to sample (ignored with --all)")
parser.add_argument("--all",    action="store_true", help="Visualise every image")
args = parser.parse_args()

splits = ["train","val"] if args.split == "both" else [args.split]

img_label_pairs = []
for split in splits:
    img_dir = DATASET_DIR / "images" / split
    lbl_dir = DATASET_DIR / "labels" / split
    for img_path in sorted(img_dir.glob("*.png")):
        lbl_path = lbl_dir / (img_path.stem + ".txt")
        img_label_pairs.append((img_path, lbl_path))

if not img_label_pairs:
    print(f"No images found in {DATASET_DIR}/images/. Run render_dataset.py first.")
    raise SystemExit(1)

if not args.all:
    random.seed(42)
    img_label_pairs = random.sample(img_label_pairs, min(args.n, len(img_label_pairs)))

OUT_DIR.mkdir(parents=True, exist_ok=True)
no_label = 0

for img_path, lbl_path in sorted(img_label_pairs):
    img = cv2.imread(str(img_path))
    H, W = img.shape[:2]

    if not lbl_path.exists() or lbl_path.read_text().strip() == "":
        no_label += 1
        cv2.putText(img, "NO LABEL", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    else:
        for line in lbl_path.read_text().strip().splitlines():
            parts = line.split()
            if len(parts) != 5:
                continue
            cls_id = int(parts[0])
            cx, cy, bw, bh = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
            x1 = int((cx - bw / 2) * W)
            y1 = int((cy - bh / 2) * H)
            x2 = int((cx + bw / 2) * W)
            y2 = int((cy + bh / 2) * H)
            color = PALETTE[cls_id % len(PALETTE)]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            label = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else str(cls_id)
            cv2.putText(img, label, (x1, max(y1 - 8, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

    out_path = OUT_DIR / img_path.name
    cv2.imwrite(str(out_path), img)

print(f"Saved {len(img_label_pairs)} annotated images → {OUT_DIR}")
print(f"  Images with no label: {no_label} / {len(img_label_pairs)}")
print(f"  Open a few to check boxes are tight around the objects.")
