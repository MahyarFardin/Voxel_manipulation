import os
import sys
import numpy as np
import torch
import sam3

from PIL import Image
from typing import List

from sam3 import build_sam3_image_model
from sam3.train.data.collator import collate_fn_api as collate
from sam3.model.utils.misc import copy_data_to_device
from sam3.train.data.sam3_image_dataset import InferenceMetadata, FindQueryLoaded, Image as SAMImage, Datapoint
from sam3.train.transforms.basic_for_api import ComposeAPI, RandomResizeAPI, ToTensorAPI, NormalizeAPI
from sam3.eval.postprocessors import PostProcessImage
from sam3.visualization_utils import plot_results


class Sam3ImagePipeline:

    def __init__(self, bpe_path: str, confidence_threshold: float = 0.5):
        self._counter = 1
        self._sam3_root = os.path.join(os.path.dirname(sam3.__file__), "..")
        sys.path.append(f"{self._sam3_root}/examples")

        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
        torch.inference_mode().__enter__()

        self.model = build_sam3_image_model(bpe_path=bpe_path)

        self.transform = ComposeAPI(transforms=[
            RandomResizeAPI(sizes=1008, max_size=1008, square=True, consistent_transform=False),
            ToTensorAPI(),
            NormalizeAPI(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ])

        self.postprocessor = PostProcessImage(
            max_dets_per_img=-1,
            iou_type="segm",
            use_original_sizes_box=True,
            use_original_sizes_mask=True,
            convert_mask_to_rle=False,
            detection_threshold=confidence_threshold,
            to_cpu=False,
        )

    def run(self, images: np.ndarray, prompt: str):
        datapoints, ids = self._prepare_datapoints(images, prompt)
        processed_results = self._inference(datapoints)
        return processed_results, ids

    def visualize(self, image: np.ndarray, processed_results: dict, query_id: int):
        plot_results(Image.fromarray(image), processed_results[query_id])

    def _prepare_datapoints(self, images: np.ndarray, prompt: str):
        datapoints, ids = [], []

        for frame in images:
            pil_image = Image.fromarray(frame)
            datapoint = self._create_datapoint(pil_image)
            ids.append(self._add_text_prompt(datapoint, prompt))
            datapoints.append(self.transform(datapoint))

        return datapoints, ids

    def _inference(self, datapoints: list):
        batch = collate(datapoints, dict_key="dummy")["dummy"]
        batch = copy_data_to_device(batch, torch.device("cuda"), non_blocking=True)

        with torch.no_grad():
            output = self.model(batch)

        return self.postprocessor.process_results(output, batch.find_metadatas)

    def _create_datapoint(self, pil_image: Image.Image) -> Datapoint:
        w, h = pil_image.size
        datapoint = Datapoint(find_queries=[], images=[])
        datapoint.images = [SAMImage(data=pil_image, objects=[], size=[h, w])]
        return datapoint

    def _add_text_prompt(self, datapoint: Datapoint, text_query: str) -> int:
        assert len(datapoint.images) == 1

        w, h = datapoint.images[0].size
        datapoint.find_queries.append(FindQueryLoaded(
            query_text=text_query,
            image_id=0,
            object_ids_output=[],
            is_exhaustive=True,
            query_processing_order=0,
            inference_metadata=InferenceMetadata(
                coco_image_id=self._counter,
                original_image_id=self._counter,
                original_category_id=1,
                original_size=[w, h],
                object_id=0,
                frame_index=0,
            )
        ))

        self._counter += 1
        return self._counter - 1

    def _add_visual_prompt(self, datapoint: Datapoint, boxes: List[List[float]],
                           labels: List[bool], text_prompt: str = "visual") -> int:
        assert len(datapoint.images) == 1
        assert len(boxes) > 0
        assert len(boxes) == len(labels)
        for b in boxes:
            assert len(b) == 4

        labels_tensor = torch.tensor(labels, dtype=torch.bool).view(-1)
        if not labels_tensor.any().item() and text_prompt == "visual":
            print("Warning: no positive box nor text prompt provided. Results will be undefined.")

        w, h = datapoint.images[0].size
        datapoint.find_queries.append(FindQueryLoaded(
            query_text=text_prompt,
            image_id=0,
            object_ids_output=[],
            is_exhaustive=True,
            query_processing_order=0,
            input_bbox=torch.tensor(boxes, dtype=torch.float).view(-1, 4),
            input_bbox_label=labels_tensor,
            inference_metadata=InferenceMetadata(
                coco_image_id=self._counter,
                original_image_id=self._counter,
                original_category_id=1,
                original_size=[w, h],
                object_id=0,
                frame_index=0,
            )
        ))

        self._counter += 1
        return self._counter - 1


if __name__ == "__main__":
    images = np.load("../environment_generation/generated_envs/image_0.npy")
    bpe_path = "/media/g3/mahyar/Voxel_manipulation/sam3/sam3/assets/bpe_simple_vocab_16e6.txt.gz"

    pipeline = Sam3ImagePipeline(bpe_path=bpe_path, confidence_threshold=0.5)
    processed_results, ids = pipeline.run(images, prompt="all the objects in different colors")

    # pipeline.visualize(images[1], processed_results, ids[1])