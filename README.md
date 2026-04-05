# Voxel Manipulation Pipeline

A robotics pipeline for generating cluttered table environments, segmenting objects, reconstructing point clouds, and generating grasps for manipulation.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Data Generation

Generate voxel assets using the notebooks and scripts in the [voxel_generation/](voxel_generation/) folder.

Once voxels are ready:

- **Single environment**: Run [environment_generation/PandaTableVoxelClutterGenerator.py](environment_generation/PandaTableVoxelClutterGenerator.py) to generate a single cluttered table scene.
- **Batch generation**: Run [environment_generation/Batch_generator.py](environment_generation/Batch_generator.py) to generate multiple environment samples along with their corresponding depth maps and RGB images.

---

## Segmentation

Follow the [SAM3 documentation](https://github.com/facebookresearch/sam3) and install SAM3 dependencies before running segmentation.

After installing dependencies:

- **Batched inference** (multiple images): [segmentation/sam3_image_batched_inference.ipynb](segmentation/sam3_image_batched_inference.ipynb)
- **Single image inference**: [segmentation/sam3_image_predictor_example.ipynb](segmentation/sam3_image_predictor_example.ipynb)

---

## Point Cloud Generation

Generate point clouds from depth maps and segmentation outputs using the scripts in [point_cloud_generation/](point_cloud_generation/).

- **From depth map**: Run [point_cloud_generation/Point_cloud_depth_map.py](point_cloud_generation/Point_cloud_depth_map.py) to reconstruct a point cloud from a depth image.
- **From segmentation map**: Run [point_cloud_generation/Point_cloud_segment_map.py](point_cloud_generation/Point_cloud_segment_map.py) to generate per-object point clouds using segmentation masks.
- For an interactive walkthrough, see [point_cloud_generation/main.ipynb](point_cloud_generation/main.ipynb).

---

## Grasp Generation

## Manipulation

