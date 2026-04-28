import numpy as np
import open3d as o3d
import pickle
import robotic as ry
from scipy.spatial.transform import Rotation


class PointCloudFromSegmentation:

    def __init__(self, fx: float, fy: float, cx: float, cy: float):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy

    @staticmethod
    def pose_to_matrix(pose: np.ndarray) -> np.ndarray:
        """
        Convert a rai pose [x, y, z, qw, qx, qy, qz] to a 4x4 camera-to-world matrix.
        """
        t = pose[:3]
        qw, qx, qy, qz = pose[3], pose[4], pose[5], pose[6]
        R = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()  # scipy uses [x,y,z,w]
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = t
        return T

    def depth_to_point_cloud(self, depth_map: np.ndarray, mask: np.ndarray = None,
                              cam_to_world: np.ndarray = None):
        H, W = depth_map.shape
        u, v = np.meshgrid(np.arange(W), np.arange(H))

        if mask is not None:
            u, v = u[mask], v[mask]
            d = depth_map[mask]
        else:
            u, v = u.flatten(), v.flatten()
            d = depth_map.flatten()

        valid = d > 0
        u, v, d = u[valid], v[valid], d[valid]

        x = (u - self.cx) * d / self.fx
        y = (v - self.cy) * d / self.fy
        z = d

        points_cam = np.stack([x, y, z], axis=-1)  # (N, 3) camera space
        coords = np.stack([v, u], axis=-1)           # (N, 2) (row, col) for color lookup

        if cam_to_world is not None:
            ones = np.ones((len(points_cam), 1))
            points_h = np.hstack([points_cam, ones])          # (N, 4)
            points_world = (cam_to_world @ points_h.T).T[:, :3]  # (N, 3)
            return points_world, coords

        return points_cam, coords

    def _compress_segments(self, masks: np.ndarray) -> np.ndarray:
        """
        Convert (N_det, 1, H, W) boolean masks into a single (H, W) integer label map.
        Pixel value = segment index (1-based); 0 = background.
        Later masks override earlier ones where they overlap.
        """
        N, _, H, W = masks.shape
        label_map = np.zeros((H, W), dtype=np.int32)
        for seg_idx in range(N):
            mask = masks[seg_idx, 0].astype(bool)
            label_map[mask] = seg_idx + 1
        return label_map

    def segment_to_point_cloud(self, depth_map: np.ndarray, segment_map: np.ndarray,
                                rgb_image: np.ndarray = None,
                                cam_to_world: np.ndarray = None):
        segment_ids = np.unique(segment_map)
        result = {}

        for seg_id in segment_ids:
            mask = segment_map == seg_id
            points, coords = self.depth_to_point_cloud(depth_map, mask=mask,
                                                        cam_to_world=cam_to_world)

            colors = None
            if rgb_image is not None and len(points) > 0:
                rows, cols = coords[:, 0], coords[:, 1]
                colors = rgb_image[rows, cols].astype(np.float32) / 255.0

            result[seg_id] = {"points": points, "colors": colors}

        return result

    def merge_all_segments(self, segment_clouds: dict):
        all_points, all_colors = [], []

        for seg in segment_clouds.values():
            if len(seg["points"]) == 0:
                continue
            all_points.append(seg["points"])
            if seg["colors"] is not None:
                all_colors.append(seg["colors"])

        if not all_points:
            return np.zeros((0, 3)), None

        merged_points = np.vstack(all_points)
        merged_colors = np.vstack(all_colors) if all_colors else None

        return merged_points, merged_colors

    def to_open3d(self, points: np.ndarray, colors: np.ndarray = None):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        if colors is not None:
            pcd.colors = o3d.utility.Vector3dVector(colors)
        return pcd

    def run(self, depth_maps: np.ndarray, all_masks: list,
            rgb_images: np.ndarray = None, cam_poses: list = None,
            visualize: bool = False):
        """
        Process all camera views and merge into one point cloud in world coordinates.

        Args:
            depth_maps:  (N_cams, H, W) float32
            all_masks:   list of N_cams arrays, each (N_det, 1, H, W) bool
            rgb_images:  (N_cams, H, W, 3) uint8 or None
            cam_poses:   list of N_cams rai poses [x, y, z, qw, qx, qy, qz]
                         or 4x4 camera-to-world matrices.
                         Without this, each view stays in its own camera frame (wrong).
            visualize:   whether to call o3d.visualization.draw_geometries
        Returns:
            pcd, merged_points, merged_colors
        """
        # Pre-build 4x4 camera-to-world matrices
        cam_to_world_list = None
        if cam_poses is not None:
            cam_to_world_list = []
            for pose in cam_poses:
                pose = np.asarray(pose)
                if pose.shape == (4, 4):
                    cam_to_world_list.append(pose)
                else:
                    cam_to_world_list.append(self.pose_to_matrix(pose))

        all_points, all_colors = [], []

        for cam_idx in range(len(all_masks)):
            depth_map    = depth_maps[cam_idx]
            masks        = all_masks[cam_idx]
            rgb_image    = rgb_images[cam_idx] if rgb_images is not None else None
            cam_to_world = cam_to_world_list[cam_idx] if cam_to_world_list is not None else None

            segment_map    = self._compress_segments(masks)
            segment_clouds = self.segment_to_point_cloud(depth_map, segment_map,
                                                          rgb_image, cam_to_world)
            cam_points, cam_colors = self.merge_all_segments(segment_clouds)

            all_points.append(cam_points)
            if cam_colors is not None:
                all_colors.append(cam_colors)

        merged_points = np.vstack(all_points)
        merged_colors = np.vstack(all_colors) if all_colors else None

        pcd = self.to_open3d(merged_points, merged_colors)

        if visualize:
            o3d.visualization.draw_geometries([pcd])

        return pcd, merged_points, merged_colors


if __name__ == "__main__":
    fx, fy, cx, cy = 4635.0, 4635.0, 960.0, 960.0

    depth_maps = np.load("../environment_generation/generated_envs/depth_0.npy")
    rgb_images = np.load("../environment_generation/generated_envs/image_0.npy")

    with open("../segmentation/output.pkl", "rb") as f:
        data = pickle.load(f)

    all_masks = [data[k]['masks'].cpu().numpy() for k in sorted(data.keys())]

    C = ry.Config()
    C.addFile("../environment_generation/generated_envs/env_0.g")
    cam_poses = [C.getFrame(f"cam_dim_{i}").getPose() for i in range(len(all_masks))]

    reconstructor = PointCloudFromSegmentation(fx=fx, fy=fy, cx=cx, cy=cy)
    pcd, points, colors = reconstructor.run(depth_maps, all_masks, rgb_images,
                                             cam_poses=cam_poses, visualize=False)

    print(f"Total points: {points.shape[0]}")
    o3d.io.write_point_cloud("output.ply", pcd)
    print("Saved output.ply")
