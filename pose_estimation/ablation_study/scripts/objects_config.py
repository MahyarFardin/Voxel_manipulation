import numpy as np

OBJECTS = {
    "lamp": {
        "scene_name":  "goal_yellow_lamp_9_mesh",
        "mesh_input":  "lamp/lamp_0001.off",
        "meshscale":   0.000271579,
        "prompt":      "yellow lamp",
        "gt_pose":     [-0.620966, -0.342511,  0.671156,
                         0.287543, -0.46152,   0.714029,  0.441],
    },
    "redcup": {
        "scene_name":  "obj_4_mesh",
        "mesh_input":  "redCup/RedCup_25k_tex.obj",
        "meshscale":   0.000943656,
        "prompt":      "red cup",
        "gt_pose":     [-0.766106,  0.0430321,  0.662863,
                         0.405586,  0.0953958,  0.909048,  -0.00559083],
    },
    "bottle": {
        "scene_name":  "obj_6_mesh",
        "mesh_input":  "bottle/Sprudelflasche_25k_tex.obj",
        "meshscale":   0.000871165,
        "prompt":      "bottle",
        "gt_pose":     [-0.412714, -0.14204,   0.7022,
                         0.179431,  0.362387,   0.857374,  -0.31842],
    },
    "crackerbox": {
        "scene_name":  "obj_7_mesh",
        "mesh_input":  "crackerBox/visual_hull_refined_smoothed.obj",
        "meshscale":   0.542528,
        "prompt":      "cracker box",
        "gt_pose":     [-0.300405, -0.26738,   0.686777,
                         0.669071,  -0.574557,  0.385652,  0.271111],
    },
}

ADD_THRESHOLD_FRACTION = 0.10   

def gt_pose_to_matrix(pose_7d: list) -> np.ndarray:
    from scipy.spatial.transform import Rotation
    pos = np.array(pose_7d[:3])
    qw, qx, qy, qz = pose_7d[3], pose_7d[4], pose_7d[5], pose_7d[6]
    R = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3]  = pos
    return T


def rotation_error_deg(R_est: np.ndarray, R_gt: np.ndarray) -> float:
    R_rel = R_est.T @ R_gt
    cos_angle = np.clip((np.trace(R_rel) - 1) / 2, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


def position_error_cm(pos_est: np.ndarray, pos_gt: np.ndarray) -> float:
    return float(np.linalg.norm(pos_est - pos_gt) * 100)


def object_diameter(vertices: np.ndarray) -> float:
    lo, hi = vertices.min(axis=0), vertices.max(axis=0)
    return float(np.linalg.norm(hi - lo))


def add_score(vertices: np.ndarray, T_est: np.ndarray, T_gt: np.ndarray):
    verts = np.asarray(vertices, dtype=np.float64)
    pts_est = (T_est[:3, :3] @ verts.T + T_est[:3, 3:]).T
    pts_gt  = (T_gt[:3, :3]  @ verts.T + T_gt[:3, 3:]).T
    add     = float(np.linalg.norm(pts_est - pts_gt, axis=1).mean())
    diam    = object_diameter(verts)
    success = add < ADD_THRESHOLD_FRACTION * diam
    return add * 100, diam * 100, success   # convert to cm
