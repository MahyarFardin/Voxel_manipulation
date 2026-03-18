from PandaTableVoxelClutterGenerator import PandaTableVoxelClutterGenerator
import robotic as ry
import numpy as np
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
        if "l_" in frame or "target" in frame or frame in ['cameraTop', 'cameraWrist', 'panda_collCameraWrist']:
            C.delFrame(frame)

def main(idx):
    # ------------------------------------------------------------
    # Create the generator
    # ------------------------------------------------------------
    generator = PandaTableVoxelClutterGenerator(
        base_scene_file=ry.raiPath("../rai-robotModels/scenarios/pandaSingle.g"),
        voxel_dir="../../voxel_generation/data/",   # folder containing voxel .g files
        output_dir="./generated_envs",
        table_frame_name="table",
        gap=0.04,
        spawn_height=0.55,
        seed=14,
        per_cube_mass=0.2,
        table_shape_size=(1.6, 1.6, 0.08, 0.02),
        panda_base_relative_pos=(0.0, 0.0, 0.05),
        marker_thickness=0.004,
        spawn_half_mode="back",   # None, "left", "right", "front", "back"
    )

    # ------------------------------------------------------------
    # Generate one environment
    # ------------------------------------------------------------
    C, summary = generator.create_environment_with_refill(
        num_voxels=int(np.random.normal(10, 4)),
        sim_seconds=10.0,
        sim_dt=0.01,
        max_refill_rounds=10,
        xy_margin=0.02,
        z_tolerance=0.15,
        batch_spawn_count=5,
        add_target_surface=True,
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
        
    np.save(f"./image_{idx}.npy", np.array(image_list))
    np.save(f"./depth_{idx}.npy", np.array(depth_list))

    saved_path = generator.save_environment(
        C,
        file_name=f"env_{idx}.g",
    )
    del C

    
if __name__ == "__main__":
    for idx in tqdm(range(1000)):
        main(idx)