import re

import numpy as np
import robotic as ry
from tqdm import tqdm

from PandaTableMeshClutterGenerator import PandaTableMeshClutterGenerator


def get_img(C: ry.Config, camera_view: ry.CameraView = None, cam_f: str = "cam0"):
    if camera_view is None:
        camera_view = ry.CameraView(C)

    cam = C.getFrame(cam_f)
    camera_view.setCamera(cam)
    img, depth = camera_view.computeImageAndDepth(C)
    img = np.asarray(img)
    return img, depth, camera_view


def remove_panda(C: ry.Config):
    for frame in list(C.getFrameNames()):
        if re.search(r"^l_|^(cameraTop|cameraWrist|panda_collCameraWrist)$", frame):
            C.delFrame(frame)


def add_capture_cameras(C: ry.Config):
    C.addFrame(
        name="cam_dim_0",
        parent="world",
        args='Q:"t(0 0 5) d(180 1 0 0)", shape:camera, size=[1], width:1920, height:1920',
    )
    C.addFrame(
        name="cam_dim_1",
        parent="world",
        args='Q:"t(0 5 1.5) d(180 1 0 0) d(-75 1 0 0) d(180 0 0 1)", shape:camera, size=[1], width:1920, height:1920',
    )
    C.addFrame(
        name="cam_dim_2",
        parent="world",
        args='Q:"t(0 -5 1.5) d(165 1 0 0) d(90 1 0 0)", shape:camera, width:1920, height:1920',
    )
    C.addFrame(
        name="cam_dim_3",
        parent="world",
        args='Q:"t(5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(195 0 0 1) d(90 0 1 0)", shape:camera, width:1920, height:1920',
    )
    C.addFrame(
        name="cam_dim_4",
        parent="world",
        args='Q:"t(-5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(165 0 0 1) d(-90 0 1 0)", shape:camera, width:1920, height:1920',
    )


def main(idx: int):
    generator = PandaTableMeshClutterGenerator(
        base_scene_file=ry.raiPath("../rai-robotModels/scenarios/pandaSingle.g"),
        dataset_dir="mesh_dataset",
        scaling_json_path="mesh_scaling_results.json",
        output_dir="./generated_envs",
        table_frame_name="table",
        gap=0.04,
        spawn_height=0.42,
        seed=42 + idx,
        object_mass=0.1,
        table_shape_size=(1.6, 1.6, 0.08, 0.02),
        panda_base_relative_pos=(0.0, 0.0, 0.05),
        target_alpha=0.35,
        target_center_jitter_ratio=0.05,
        clutter_mode="high_clutter",
        placement_candidate_count=128,
        hardnessOfTargetObject=0.0,
    )

    C, summary = generator.create_environment_with_refill(
        num_voxels=8,
        sim_seconds=10.0,
        sim_dt=0.01,
        max_refill_rounds=10,
        xy_margin=0.02,
        z_tolerance=0.15,
        batch_spawn_count=5,
        max_target_spawn_attempts=40,
    )

    remove_panda(C)
    add_capture_cameras(C)

    depth_list = []
    image_list = []
    camera_view = None

    for i in range(5):
        img, depth, camera_view = get_img(C=C, camera_view=camera_view, cam_f=f"cam_dim_{i}")
        image_list.append(img)
        depth_list.append(depth)

    np.save(f"./generated_envs/image_{idx}.npy", np.array(image_list))
    np.save(f"./generated_envs/depth_{idx}.npy", np.array(depth_list))

    saved_path = generator.save_environment(
        C,
        file_name=f"env_{idx}.g",
    )

    del C
    return saved_path, summary


if __name__ == "__main__":
    for idx in tqdm(range(20)):
        main(idx)
