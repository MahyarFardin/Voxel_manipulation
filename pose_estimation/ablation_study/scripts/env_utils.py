import json
from pathlib import Path


def load_camera_info_for_env(cam_info_path, env_name, project_root):
    with open(cam_info_path) as f:
        camera_info = json.load(f)

    if env_name is None:
        return camera_info

    project_root = Path(project_root)
    depth_dir    = project_root / "yolo_dataset" / "depth"

    img_dir = None
    for split in ("val", "train"):
        candidate = project_root / "yolo_dataset" / "images" / split
        if (candidate / f"{env_name}_cam_dim_0.png").exists():
            img_dir = candidate
            break

    if img_dir is None:
        raise FileNotFoundError(
            f"No images found for '{env_name}' in yolo_dataset/images/val or train.\n"
            f"Expected files like: {project_root}/yolo_dataset/images/val/{env_name}_cam_dim_0.png"
        )

    new_info = {}
    for cam_name, info in camera_info.items():
        new_info[cam_name] = dict(info)
        new_info[cam_name]["rgb_path"]   = str(img_dir  / f"{env_name}_{cam_name}.png")
        new_info[cam_name]["depth_path"] = str(depth_dir / f"{env_name}_{cam_name}.npy")

    return new_info
