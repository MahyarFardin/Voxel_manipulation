import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
from sam3 import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor
from sam3.visualization_utils import plot_results


class Sam3Pipeline:

    def __init__(self, bpe_path: str, confidence_threshold: float = 0.5, iou_threshold: float = 0.5):
        self.iou_threshold = iou_threshold

        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.autocast("cuda", dtype=torch.bfloat16).__enter__()

        self.model = build_sam3_image_model(bpe_path=bpe_path)
        self.processor = Sam3Processor(self.model, confidence_threshold=confidence_threshold)

    def run(self, image_path: str, prompt: str):
        image = Image.open(image_path).convert("RGB")

        inference_state = self.processor.set_image(image)
        self.processor.reset_all_prompts(inference_state)
        inference_state = self.processor.set_text_prompt(state=inference_state, prompt=prompt)

        plot_results(Image.open(image_path), inference_state)

        kept_indices = self._nms(inference_state["boxes"], inference_state["scores"])
        kept_boxes = [inference_state["boxes"][i].cpu().numpy() for i in kept_indices]
        segment_maps = [inference_state["masks"][i].cpu().numpy() for i in kept_indices]

        self._plot_boxes(image_path, kept_boxes)

        seg_map = self.masks_to_segmentation_map(segment_maps)  # <-- new

        return kept_boxes, segment_maps, seg_map

    def _nms(self, boxes, scores):
        if not isinstance(boxes, torch.Tensor):
            boxes = torch.tensor(boxes, dtype=torch.float32)
        if not isinstance(scores, torch.Tensor):
            scores = torch.tensor(scores, dtype=torch.float32)

        x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort(descending=True)

        kept = []
        while order.numel() > 0:
            i = order[0].item()
            kept.append(i)

            if order.numel() == 1:
                break

            inter_x1 = x1[order[1:]].clamp(min=x1[i])
            inter_y1 = y1[order[1:]].clamp(min=y1[i])
            inter_x2 = x2[order[1:]].clamp(max=x2[i])
            inter_y2 = y2[order[1:]].clamp(max=y2[i])

            inter = (inter_x2 - inter_x1).clamp(min=0) * (inter_y2 - inter_y1).clamp(min=0)
            iou = inter / (areas[i] + areas[order[1:]] - inter)

            order = order[1:][iou <= self.iou_threshold]

        return kept
    
    def masks_to_segmentation_map(self, segment_maps: list) -> np.ndarray:
        H, W = segment_maps[0].shape[-2], segment_maps[0].shape[-1]
        seg_map = np.zeros((H, W), dtype=np.int32)

        for seg_id, mask in enumerate(segment_maps, start=1):
            mask = np.array(mask).squeeze()
            seg_map[mask.astype(bool)] = seg_id

        return seg_map

    def _plot_boxes(self, image_path: str, boxes):
        image = Image.open(image_path)

        if isinstance(boxes, torch.Tensor):
            boxes = boxes.detach().cpu().numpy()

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.imshow(image)

        for i, (x1, y1, x2, y2) in enumerate(boxes):
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2, edgecolor='red', facecolor='none'
            )
            ax.add_patch(rect)
            ax.text(x1, y1 - 5, str(i), color='red', fontsize=10, fontweight='bold')

        ax.axis('off')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    pipeline = Sam3Pipeline(
        bpe_path="../sam3/sam3/assets/bpe_simple_vocab_16e6.txt.gz",
        confidence_threshold=0.5,
        iou_threshold=0.5
    )

    kept_boxes, segment_maps = pipeline.run(
        image_path="../segmentation/sample_segmentation_img.png",
        prompt="all the objects in different colors"
    )