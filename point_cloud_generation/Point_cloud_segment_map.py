import numpy as np
import open3d as o3d


class PointCloudFromSegmentation:

    def __init__(self, fx: float, fy: float, cx: float, cy: float):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy

    def depth_to_point_cloud(self, depth_map: np.ndarray, mask: np.ndarray = None):
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

        points = np.stack([x, y, z], axis=-1)
        coords = np.stack([v, u], axis=-1)

        return points, coords

    def segment_to_point_cloud(self, depth_map: np.ndarray, segment_map: np.ndarray, rgb_image: np.ndarray = None):

        segment_ids = np.unique(segment_map)
        result = {}

        for seg_id in segment_ids:
            mask = segment_map == seg_id
            points, coords = self.depth_to_point_cloud(depth_map, mask=mask)

            colors = None
            if rgb_image is not None:
                rows, cols = coords[:, 0], coords[:, 1]
                valid_depth_mask = depth_map[mask] > 0
                colors = rgb_image[rows, cols][valid_depth_mask]
                colors = colors / 255.0

            result[seg_id] = {"points": points, "colors": colors}

        return result

    def merge_all_segments(self, segment_clouds: dict):

        all_points, all_colors = [], []

        for seg in segment_clouds.values():
            all_points.append(seg["points"])
            if seg["colors"] is not None:
                all_colors.append(seg["colors"])

        merged_points = np.vstack(all_points)
        merged_colors = np.vstack(all_colors) if all_colors else None

        return merged_points, merged_colors

    def to_open3d(self, points: np.ndarray, colors: np.ndarray = None):

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        if colors is not None:
            pcd.colors = o3d.utility.Vector3dVector(colors)
        return pcd

    def run(self, depth_map: np.ndarray, segment_map: np.ndarray,
            rgb_image: np.ndarray = None, visualize: bool = False):

        segment_clouds = self.segment_to_point_cloud(depth_map, segment_map, rgb_image)
        merged_points, merged_colors = self.merge_all_segments(segment_clouds)
        pcd = self.to_open3d(merged_points, merged_colors)

        if visualize:
            o3d.visualization.draw_geometries([pcd])

        return pcd, merged_points, merged_colors


if __name__ == "__main__":
    H, W = 480, 640
    fx, fy, cx, cy = 525.0, 525.0, 319.5, 239.5

    depth_map   = np.random.uniform(0.5, 5.0, (H, W)).astype(np.float32)
    segment_map = np.random.randint(0, 5, (H, W)).astype(np.int32)
    rgb_image   = np.random.randint(0, 255, (H, W, 3)).astype(np.uint8)

    reconstructor = PointCloudFromSegmentation(fx=fx, fy=fy, cx=cx, cy=cy)
    pcd, points, colors = reconstructor.run(depth_map, segment_map, rgb_image, visualize=True)

    print(f"Total points: {points.shape[0]}")
    o3d.io.write_point_cloud("output.ply", pcd)