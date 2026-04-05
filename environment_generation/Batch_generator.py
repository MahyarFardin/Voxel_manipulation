from PandaTableVoxelClutterGenerator import PandaTableVoxelClutterGenerator
import robotic as ry
import numpy as np
import re
from tqdm import tqdm

def get_img(C:ry.Config, camera_view:ry.CameraView=None, cam_f:str="cam0"):
    if camera_view is None:
        camera_view = ry.CameraView(C)
    cam = C.getFrame(cam_f)
    camera_view.setCamera(cam)
    img, depth = camera_view.computeImageAndDepth(C)
    img = np.asarray(img)
    return img, depth, camera_view

def calculate_center_of_pile(C):
    min_corner = np.array([np.inf, np.inf, np.inf])
    max_corner = np.array([-np.inf, -np.inf, -np.inf])
    
    for f in C.getFrames():
        size = f.getSize()
        if size is None or len(size) < 3:
            continue
    
        pos = np.array(f.getPosition())
    
        half = np.array(size[:3]) / 2
    
        min_corner = np.minimum(min_corner, pos - half)
        max_corner = np.maximum(max_corner, pos + half)
    
    return (max_corner + min_corner) / 2

def remove_panda(C):
    for frame in C.getFrameNames():
        if re.search(r'^l_|target|^(cameraTop|cameraWrist|panda_collCameraWrist)$', frame):
            C.delFrame(frame)

def main(idx):

    generator = PandaTableVoxelClutterGenerator(
        base_scene_file=ry.raiPath("../rai-robotModels/scenarios/pandaSingle.g"),  # Path to the base Panda scene file
        voxel_dir="../voxel_generation/data",                                        # Directory containing voxel .g files
        output_dir="./generated_envs",                                               # Directory where generated environments will be saved
        table_frame_name="table",                                                    # Name of the table frame inside the scene
        gap=0.04,                                                                    # Spacing margin used around objects / boundaries in placement logic
        spawn_height=0.41,                                                           # Extra height above the table used when initially dropping voxels
        seed=42,                                                                      # Random seed for reproducible scene generation
        per_cube_mass=0.2,                                                           # Mass assigned to each cube piece of a voxel object
        table_shape_size=(1.6, 1.6, 0.08, 0.02),                                    # Table size/shape parameters passed to the table ssBox
        panda_base_relative_pos=(0.0, 0.0, 0.05),                                   # Relative position offset applied to the Panda base
        target_alpha=0.9,                                                            # Alpha/transparency value used for the target voxel cubes
        target_center_jitter_ratio=0.05,                                             # Small random jitter ratio around the center of the target quarter
        clutter_mode="high_clutter",                                                 # Clutter placement mode: "random", "low_clutter", or "high_clutter"
        placement_candidate_count=128,                                               # Number of sampled candidates used mainly in low/high clutter placement
    )

    C, summary = generator.create_environment_with_refill(
        num_voxels=8,                # Total number of voxels in the final scene, including the target
        sim_seconds=10.0,            # Physics simulation duration per round in seconds
        sim_dt=0.01,                 # Physics simulation timestep
        max_refill_rounds=10,        # Maximum number of clutter refill/simulate rounds
        xy_margin=0.02,              # XY table boundary margin used when checking whether objects stayed on the table
        z_tolerance=0.15,            # Allowed drop below table-top threshold before object is considered off-table
        batch_spawn_count=5,         # Maximum number of clutter voxels spawned in one refill batch
    )

    remove_panda(C)

    box_center = calculate_center_of_pile(C)
    
    C.addFrame(name="cam_dim_0", parent="world", args='Q:"t(0 0 5) d(180 1 0 0)", shape:camera, size=[1], width:1920, height:1920')
    C.addFrame(name="cam_dim_1", parent="world", args='Q:"t(0 5 1.5) d(180 1 0 0) d(-75 1 0 0) d(180 0 0 1)", shape:camera, size=[1], width:1920, height:1920')
    C.addFrame(name="cam_dim_2", parent="world", args='Q:"t(0 -5 1.5) d(165 1 0 0) d(90 1 0 0)", shape:camera, width:1920, height:1920')
    C.addFrame(name="cam_dim_3", parent="world", args='Q:"t(5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(195 0 0 1) d(90 0 1 0)", shape:camera, width:1920, height:1920')
    C.addFrame(name="cam_dim_4", parent="world", args='Q:"t(-5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(165 0 0 1) d(-90 0 1 0)", shape:camera, width:1920, height:1920')

    depth_list = []
    image_list = []
    
    for i in range(5):
        t = get_img(C=C, cam_f = f"cam_dim_{i}")
        image_list.append(t[0])
        depth_list.append(t[1])
        
    np.save(f"./generated_envs/image_{idx}.npy", np.array(image_list))
    np.save(f"./generated_envs/depth_{idx}.npy", np.array(depth_list))

    saved_path = generator.save_environment(
        C,
        file_name=f"env_{idx}.g",
    )
    del C

    
if __name__ == "__main__":
    for idx in tqdm(range(20)):
        main(idx)