import numpy as np
import robotic as ry
from pyvirtualdisplay import Display


class PointCloudReconstructor:
    def __init__(self):
        pass

    def calculate_center_of_pile(self, C: ry.Config):
        min_corner = np.array([np.inf, np.inf, np.inf])
        max_corner = np.array([-np.inf, -np.inf, -np.inf])
        
        for f in C.getFrameNames():
            size = C.getFrame(f).getSize()
            f = C.getFrame(f)
            if size is None or size.shape == () or len(size) < 3:
                continue
        
            pos = np.array(f.getPosition())
        
            half = np.array(size[:3]) / 2
        
            min_corner = np.minimum(min_corner, pos - half)
            max_corner = np.maximum(max_corner, pos + half)
        
        return (max_corner + min_corner) / 2
    
    def config_to_point_cloud(self, C: ry.Config, camera_frame: str):
        cam = ry.CameraView(C)
        cam.setCamera(C.getFrame(camera_frame))

        rgb, depth = cam.computeImageAndDepth(C)
        fxycxy = cam.getFxycxy()

        frame = C.getFrame(camera_frame)
        T = frame.getPosition()
        R = frame.getRotationMatrix()

        points_raw = ry.depthImage2PointCloud(depth, fxycxy)

        # Normalize to (N, 3)
        if points_raw.ndim == 3:
            points_cam = points_raw.reshape(-1, 3)
        elif points_raw.ndim == 2:
            if points_raw.shape[0] == 3 and points_raw.shape[1] != 3:
                points_cam = points_raw.T
            else:
                points_cam = points_raw
        else:
            raise ValueError(f"Unexpected point cloud shape: {points_raw.shape}")

        colors = rgb.reshape(-1, 3)

        # Sanity check before masking
        assert points_cam.shape[0] == colors.shape[0], \
            f"Mismatch: points {points_cam.shape} vs colors {colors.shape}"
        assert points_cam.shape[1] == 3, \
            f"points_cam should be (N,3), got {points_cam.shape}"

        mask = points_cam[:, 2] < 5
        points_cam = points_cam[mask]
        colors     = colors[mask]

        points_world = (R @ points_cam.T).T + T

        return points_world, colors

    def reconstruct_from_two_views(self, C: ry.Config):
        display = Display(visible=False, size=(1920, 1920))
        display.start()

        box_center = self.calculate_center_of_pile(C)
        C.addFrame("center_box").setPosition(box_center)

        C.addFrame(name="cam_dim_0", parent="center_box", args='Q:"t(0 0 5) d(180 1 0 0)", shape:camera, width:1920, height:1920')
        C.addFrame(name="cam_dim_1", parent="center_box", args='Q:"t(0 5 1.5) d(180 1 0 0) d(-75 1 0 0) d(180 0 0 1)", shape:camera, width:1920, height:1920')
        C.addFrame(name="cam_dim_2", parent="center_box", args='Q:"t(0 -5 1.5) d(165 1 0 0) d(90 1 0 0)", shape:camera, width:1920, height:1920')
        C.addFrame(name="cam_dim_3", parent="center_box", args='Q:"t(5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(195 0 0 1) d(90 0 1 0)", shape:camera, width:1920, height:1920')
        C.addFrame(name="cam_dim_4", parent="center_box", args='Q:"t(-5 0 1.5) d(180 1 0 0) d(-90 1 0 0) d(165 0 0 1) d(-90 0 1 0)", shape:camera, width:1920, height:1920')

        points1, colors1 = self.config_to_point_cloud(C, "cam_dim_0")
        points2, colors2 = self.config_to_point_cloud(C, "cam_dim_1")
        points3, colors3 = self.config_to_point_cloud(C, "cam_dim_2")
        points4, colors4 = self.config_to_point_cloud(C, "cam_dim_3")
        points5, colors5 = self.config_to_point_cloud(C, "cam_dim_4")

        merged_points = np.vstack([points1, points2, points3, points4, points5])
        merged_colors = np.vstack([colors1, colors2, colors3, colors4, colors5])

        display.stop()

        return merged_points, merged_colors