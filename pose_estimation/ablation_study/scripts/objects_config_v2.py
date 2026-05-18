import numpy as np

OBJECTS = {
    "lamp": {
        "scene_name": "goal_yellow_lamp_9_mesh",
        "mesh_input": "lamp/lamp_0001.off",
        "meshscale":  0.000271579,
        "prompt":     "yellow lamp",
        "yolo_class": "lamp",
        "gt_pose":    [-0.620966, -0.342511,  0.671156,
                        0.287543, -0.46152,    0.714029,  0.441],
    },
    "cone": {
        "scene_name": "obj_2_mesh",
        "mesh_input": "cone/cone_0001.off",
        "meshscale":  0.00708861,
        "prompt":     "cone",
        "yolo_class": "cone",
        "gt_pose":    [-0.491555, -0.179998,  0.710873,
                        0.14596,  -0.767228,  -0.188065, -0.595557],
    },
    "redcup": {
        "scene_name": "obj_4_mesh",
        "mesh_input": "redCup/RedCup_25k_tex.obj",
        "meshscale":  0.000943656,
        "prompt":     "red cup",
        "yolo_class": None,
        "gt_pose":    [-0.766106,  0.0430321,  0.662863,
                        0.405586,  0.0953958,  0.909048, -0.00559083],
    },
    "bottle": {
        "scene_name": "obj_6_mesh",
        "mesh_input": "bottle/Sprudelflasche_25k_tex.obj",
        "meshscale":  0.000871165,
        "prompt":     "bottle",
        "yolo_class": None,
        "gt_pose":    [-0.412714, -0.14204,    0.7022,
                        0.179431,  0.362387,   0.857374, -0.31842],
    },
    "crackerbox": {
        "scene_name": "obj_7_mesh",
        "mesh_input": "crackerBox/visual_hull_refined_smoothed.obj",
        "meshscale":  0.542528,
        "prompt":     "cracker box",
        "yolo_class": None,
        "gt_pose":    [-0.300405, -0.26738,    0.686777,
                        0.669071, -0.574557,   0.385652,  0.271111],
    },
    "deodorant": {
        "scene_name": "obj_8_mesh",
        "mesh_input": "deodorant/Deodorant_25k_tex.obj",
        "meshscale":  0.00147527,
        "prompt":     "deodorant",
        "yolo_class": None,
        "gt_pose":    [-0.128106, -0.74047,    0.681569,
                        0.235776, -0.750685,   0.420041,  0.452159],
    },
}

ADD_THRESHOLD_FRACTION = 0.10

def gt_pose_to_matrix(pose_7d):
    from scipy.spatial.transform import Rotation
    pos = np.array(pose_7d[:3])
    qw, qx, qy, qz = pose_7d[3], pose_7d[4], pose_7d[5], pose_7d[6]
    R = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3]  = pos
    return T


def rotation_error_deg(R_est, R_gt):
    R_rel     = R_est.T @ R_gt
    cos_angle = np.clip((np.trace(R_rel) - 1) / 2, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


def position_error_cm(pos_est, pos_gt):
    return float(np.linalg.norm(pos_est - pos_gt) * 100)


def object_diameter(vertices):
    lo, hi = vertices.min(axis=0), vertices.max(axis=0)
    return float(np.linalg.norm(hi - lo))


def add_score(vertices, T_est, T_gt):
    verts   = np.asarray(vertices, dtype=np.float64)
    pts_est = (T_est[:3, :3] @ verts.T + T_est[:3, 3:]).T
    pts_gt  = (T_gt[:3, :3]  @ verts.T + T_gt[:3, 3:]).T
    add     = float(np.linalg.norm(pts_est - pts_gt, axis=1).mean())
    diam    = object_diameter(verts)
    success = add < ADD_THRESHOLD_FRACTION * diam
    return add * 100, diam * 100, success

def boxes_cxcywh_to_xyxy(boxes_norm, W, H):
    import torch
    cx, cy, w, h = boxes_norm.unbind(-1)
    return torch.stack([(cx - w/2)*W, (cy - h/2)*H,
                        (cx + w/2)*W, (cy + h/2)*H], dim=-1)


def mask_to_bbox(mask):
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return None
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return np.array([cmin, rmin, cmax, rmax], dtype=float)


def depth_mask_from_bbox(depth, box_xyxy, tol=0.15):
    H, W    = depth.shape
    x1, y1, x2, y2 = box_xyxy.astype(int)
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(W - 1, x2), min(H - 1, y2)

    cx1 = x1 + int((x2 - x1) * 0.35)
    cy1 = y1 + int((y2 - y1) * 0.35)
    cx2 = x1 + int((x2 - x1) * 0.65)
    cy2 = y1 + int((y2 - y1) * 0.65)
    patch = depth[cy1:cy2, cx1:cx2]
    valid = patch[(patch > 0.05) & np.isfinite(patch)]

    mask = np.zeros((H, W), dtype=bool)
    if len(valid) == 0:
        mask[y1:y2, x1:x2] = True
        return mask

    obj_d = float(np.median(valid))
    box_d = depth[y1:y2, x1:x2]
    mask[y1:y2, x1:x2] = (
        (box_d > 0.05) & np.isfinite(box_d) &
        (np.abs(box_d - obj_d) < tol)
    )
    return mask


def cluster_estimates(estimates, dist_m=0.30):
    clusters = []
    for est in estimates:
        placed = False
        for cl in clusters:
            if np.linalg.norm(est["position"] - cl["rep"]["position"]) < dist_m:
                cl["members"].append(est)
                if est["score"] > cl["rep"]["score"]:
                    cl["rep"] = est
                placed = True
                break
        if not placed:
            clusters.append({"rep": est, "members": [est]})
    clusters.sort(key=lambda c: c["rep"]["score"], reverse=True)
    return clusters

def save_det_viz(out_path, rgb_bgr, box_xyxy, score, cam_name,
                 mask=None, color=(0, 200, 0), extra_text=""):
    import cv2
    vis = rgb_bgr.copy()
    if mask is not None:
        mask_u8  = mask.astype(np.uint8) * 255
        overlay  = np.zeros_like(vis)
        overlay[:] = color
        vis = cv2.addWeighted(vis, 1.0,
                              cv2.bitwise_and(overlay, overlay, mask=mask_u8),
                              0.4, 0)
    x1, y1, x2, y2 = box_xyxy.astype(int)
    cv2.rectangle(vis, (x1, y1), (x2, y2), color, 3)
    label = f"{cam_name}  conf={score:.3f}"
    if extra_text:
        label += f"  {extra_text}"
    cv2.putText(vis, label, (x1, max(y1 - 8, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    cv2.imwrite(str(out_path), vis)


def save_pose_viz(out_path, rgb_bgr, K, T_co, T_wo, verts_hom,
                  color=(0, 165, 255), axis_len=0.05):
    import cv2
    vis    = rgb_bgr.copy()
    H_v, W_v = vis.shape[:2]

    verts_c = (T_co @ verts_hom.T).T[:, :3]
    front   = verts_c[:, 2] > 0
    if front.any():
        pts2d = (K @ verts_c[front].T).T
        pts2d = (pts2d[:, :2] / pts2d[:, 2:3]).astype(int)
        ok    = ((pts2d[:, 0] >= 0) & (pts2d[:, 0] < W_v) &
                 (pts2d[:, 1] >= 0) & (pts2d[:, 1] < H_v))
        for pt in pts2d[ok][::10]:
            cv2.circle(vis, tuple(pt), 3, color, -1)

    def prj(p):
        q = K @ p
        return (int(q[0]/q[2]), int(q[1]/q[2]))

    o  = prj(T_co[:3, 3])
    xp = prj(T_co[:3, 3] + axis_len * T_co[:3, 0])
    yp = prj(T_co[:3, 3] + axis_len * T_co[:3, 1])
    zp = prj(T_co[:3, 3] + axis_len * T_co[:3, 2])
    cv2.arrowedLine(vis, o, xp, (0,   0, 255), 3, tipLength=0.3)
    cv2.arrowedLine(vis, o, yp, (0, 255,   0), 3, tipLength=0.3)
    cv2.arrowedLine(vis, o, zp, (255,   0,   0), 3, tipLength=0.3)

    pos = T_wo[:3, 3]
    txt = f"pos=[{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]"
    cv2.putText(vis, txt, (10, H_v - 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)
    cv2.imwrite(str(out_path), vis)
