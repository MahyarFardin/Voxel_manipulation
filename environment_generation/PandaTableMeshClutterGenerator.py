from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import uuid
from pathlib import Path
import os
import numpy as np
import robotic as ry

from rebuild_scene_from_g import _sanitize_scene_text_for_addfile, recreate_scene_from_g
from save_scene_to_g import save_config_as_g


class PandaTableMeshClutterGenerator:
    """
    Mesh-based replacement for the voxel clutter generator.

    Behavior is intentionally aligned with the old voxel version:

    1. One target object is chosen in advance from `mesh_dataset`.
    2. One random table quarter is assigned to that target.
    3. Normal clutter objects are spawned according to `clutter_mode`.
    4. A normal-opacity copy of the target object is also spawned into the
       clutter with the frame prefix `goal_`.
    5. A copy of the same target is spawned near the center of the selected
       target quarter with the frame prefix `goal_pose_`, allowed to settle in
       simulation, then switched to a non-contact translucent marker with the
       same color as the clutter-side target.
    6. `hardnessOfTargetObject` controls how early the clutter-side `goal_`
       target is inserted among clutter drops.
    7. The final scene is validated so that exactly one on-table `goal_` and
       one on-table `goal_pose_` survive.
    8. Textured meshes are loaded using absolute paths with
       `cd_into_mesh_files=False`, and saved scenes should be reloaded via
       `reload_saved_environment(...)` for safer texture/cache handling.
    """

    DEFAULT_PREFER_EXTS = (".obj", ".off", ".ply")
    GOAL_POSE_ALPHA = 0.5
    OFF_COLOR_PALETTE = (
        ("red", (1.0, 0.0, 0.0)),
        ("green", (0.0, 1.0, 0.0)),
        ("blue", (0.0, 0.0, 1.0)),
        ("yellow", (1.0, 1.0, 0.0)),
        ("orange", (1.0, 0.5, 0.0)),
        ("purple", (0.5, 0.0, 1.0)),
        ("white", (1.0, 1.0, 1.0)),
    )

    def __init__(
        self,
        base_scene_file=ry.raiPath("../rai-robotModels/scenarios/pandaSingle.g"),
        dataset_dir="mesh_dataset",
        scaling_json_path="mesh_scaling_results_bounded.json",
        output_dir="./generated_envs",
        table_frame_name="table",
        gap=0.04,
        spawn_height=0.41,
        seed=15,
        object_mass=0.2,
        table_shape_size=(1.6, 1.6, 0.08, 0.02),
        panda_base_relative_pos=(0.0, 0.0, 0.05),
        target_alpha=0.35,
        target_center_jitter_ratio=0.10,
        clutter_mode="random",
        placement_candidate_count=96,
        hardnessOfTargetObject=0.0,
        prefer_exts=DEFAULT_PREFER_EXTS,
        cache_bust_live_mesh_paths=True,
        cache_root=None,
    ):
        self.base_scene_file = Path(base_scene_file)
        self.dataset_dir = self._norm_path(dataset_dir)
        self.scaling_json_path = self._norm_path(scaling_json_path)
        self.output_dir = Path(output_dir)
        self.table_frame_name = table_frame_name
        self.gap = float(gap)
        self.spawn_height = float(spawn_height)
        self.seed = seed
        self.object_mass = float(object_mass)
        self.table_shape_size = list(table_shape_size)
        self.panda_base_relative_pos = list(panda_base_relative_pos)
        self.target_alpha = float(target_alpha)
        self.target_center_jitter_ratio = float(target_center_jitter_ratio)
        self.clutter_mode = str(clutter_mode)
        self.placement_candidate_count = int(placement_candidate_count)
        self.hardnessOfTargetObject = float(hardnessOfTargetObject)
        self.prefer_exts = tuple(str(ext).lower() for ext in prefer_exts)
        self.cache_bust_live_mesh_paths = bool(cache_bust_live_mesh_paths)
        self.cache_root = (
            self._norm_path(cache_root)
            if cache_root is not None
            else Path(tempfile.gettempdir()) / "robotic_mesh_live_cache"
        )

        if not self.base_scene_file.exists():
            raise FileNotFoundError(f"Base scene file not found: {self.base_scene_file}")
        if not self.dataset_dir.exists():
            raise FileNotFoundError(f"Dataset directory not found: {self.dataset_dir}")
        if not self.dataset_dir.is_dir():
            raise NotADirectoryError(f"Dataset path is not a directory: {self.dataset_dir}")
        if not self.scaling_json_path.exists():
            raise FileNotFoundError(
                f"Scaling JSON not found: {self.scaling_json_path}. "
                "This generator requires a precomputed scaling file."
            )

        if not (0.0 <= self.hardnessOfTargetObject <= 1.0):
            raise ValueError("hardnessOfTargetObject must be between 0 and 1.")

        allowed_modes = {"random", "low_clutter", "high_clutter"}
        if self.clutter_mode not in allowed_modes:
            raise ValueError(
                f"Unknown clutter_mode: {self.clutter_mode}. "
                f"Allowed: {sorted(allowed_modes)}"
            )

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rng = np.random.default_rng(self.seed)

        self._configure_mesh_loading()

        self.scaling_by_mesh = self._load_scaling_by_mesh(self.scaling_json_path)
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.live_mesh_cache_root = self.cache_root / f"live_{uuid.uuid4().hex}"
        self.live_mesh_cache_root.mkdir(parents=True, exist_ok=True)
        self.mesh_catalog = self._build_mesh_catalog()

        self.spawned_objects: list[dict[str, object]] = []
        self.used_object_names: set[str] = set()
        self.reserved_object_names: set[str] = set()
        self.object_counter = 0

        self.target_object = None
        self.target_quarter_mode = None
        self.target_color_name = None
        self.target_rgb = None

        self.goal_clutter_object_prefix = None
        self.goal_pose_object_prefix = None

        self.goal_clutter_insert_index = None
        self.clutter_spawn_success_count = 0
        self.goal_clutter_has_spawned_once = False

    # =========================================================
    # Setup helpers
    # =========================================================
    def _norm_path(self, path: str | Path) -> Path:
        return Path(path).expanduser().resolve(strict=False)

    def _configure_mesh_loading(self):
        ry.params_add({"cd_into_mesh_files": False})

    def _load_scaling_by_mesh(self, scaling_json_path: str | Path) -> dict[Path, dict[str, object]]:
        data = json.loads(Path(scaling_json_path).read_text())
        scaling_by_mesh: dict[Path, dict[str, object]] = {}

        for item in data:
            if "mesh_path" not in item or "scale_factor" not in item:
                raise ValueError(
                    "Each scaling JSON record must contain at least "
                    "'mesh_path' and 'scale_factor'."
                )

            mesh_path = self._norm_path(item["mesh_path"])
            scaling_by_mesh[mesh_path] = {
                **item,
                "mesh_path": mesh_path,
                "scale_factor": float(item["scale_factor"]),
            }

        return scaling_by_mesh

    def _selected_candidates_in_dir(self, object_dir: Path) -> list[Path]:
        candidates = [
            self._norm_path(p) for p in object_dir.iterdir()
            if p.is_file() and p.suffix.lower() in set(self.prefer_exts)
        ]
        ext_priority = {ext: i for i, ext in enumerate(self.prefer_exts)}
        candidates.sort(
            key=lambda p: (ext_priority.get(p.suffix.lower(), 999), p.name.lower())
        )
        return candidates

    def _mesh_local_bounds(self, mesh_path: Path, scale_factor: float):
        self._configure_mesh_loading()
        C = ry.Config()
        f = C.addFrame("tmp_mesh")
        f.setShape(ry.ST.mesh, size=1.0)
        f.setMeshFile(str(mesh_path), scale=float(scale_factor))

        V = f.getMeshPoints()
        if V is None or len(V) == 0:
            raise ValueError(f"Mesh has no vertices or could not be loaded: {mesh_path}")

        V = np.asarray(V, dtype=float)
        mins = V.min(axis=0)
        maxs = V.max(axis=0)
        return mins, maxs, maxs - mins

    def _cache_busted_mesh_path(self, mesh_path: Path) -> Path:
        mesh_path = self._norm_path(mesh_path)
        src_dir = mesh_path.parent
        digest = hashlib.sha1(str(src_dir).encode("utf-8")).hexdigest()[:12]
        dst_dir = self.live_mesh_cache_root / f"{src_dir.name}_{digest}"

        if not dst_dir.exists():
            shutil.copytree(src_dir, dst_dir)

        return dst_dir / mesh_path.name

    def _build_mesh_catalog(self) -> list[dict[str, object]]:
        object_dirs = sorted(
            [d for d in self.dataset_dir.iterdir() if d.is_dir()],
            key=lambda p: p.name.lower(),
        )

        if not object_dirs:
            raise RuntimeError(f"No object folders found in dataset: {self.dataset_dir}")

        catalog: list[dict[str, object]] = []
        failures: list[str] = []

        for object_dir in object_dirs:
            candidates = self._selected_candidates_in_dir(object_dir)
            if not candidates:
                failures.append(
                    f"{object_dir.name}: no candidate meshes found for preferred extensions "
                    f"{self.prefer_exts}"
                )
                continue

            selected_mesh = None
            selected_record = None
            for candidate in candidates:
                record = self.scaling_by_mesh.get(candidate)
                if record is not None:
                    selected_mesh = candidate
                    selected_record = record
                    break

            if selected_mesh is None or selected_record is None:
                failures.append(
                    f"{object_dir.name}: no preferred mesh has an exact entry in "
                    f"{self.scaling_json_path.name}"
                )
                continue

            is_colorable_off_object = (
                len(candidates) == 1 and selected_mesh.suffix.lower() == ".off"
            )

            local_min, local_max, computed_size_xyz = self._mesh_local_bounds(
                selected_mesh,
                float(selected_record["scale_factor"]),
            )

            scaled_size_xyz = selected_record.get("aabb_size_xyz_after_scaling")
            if scaled_size_xyz is None:
                scaled_size_xyz = computed_size_xyz.tolist()

            catalog.append(
                {
                    "object_name": object_dir.name,
                    "source_dir": object_dir,
                    "mesh_path": selected_mesh,
                    "load_mesh_path": (
                        self._cache_busted_mesh_path(selected_mesh)
                        if self.cache_bust_live_mesh_paths
                        else selected_mesh
                    ),
                    "mesh_basename": selected_mesh.name,
                    "mesh_ext": selected_mesh.suffix.lower(),
                    "is_colorable_off_object": is_colorable_off_object,
                    "scale_factor": float(selected_record["scale_factor"]),
                    "aabb_size_xyz_after_scaling": [
                        float(v) for v in scaled_size_xyz
                    ],
                    "local_aabb_min_after_scaling": [float(v) for v in local_min],
                    "local_aabb_max_after_scaling": [float(v) for v in local_max],
                    "footprint_size_xy": [
                        float(computed_size_xyz[0]),
                        float(computed_size_xyz[1]),
                    ],
                    "height_z": float(computed_size_xyz[2]),
                }
            )

        if failures:
            raise RuntimeError(
                "Mesh catalog construction failed:\n- " + "\n- ".join(failures)
            )

        if not catalog:
            raise RuntimeError(f"No usable mesh objects found in dataset: {self.dataset_dir}")

        return catalog

    def _load_base_scene(self):
        C = ry.Config()
        C.addFile(str(self.base_scene_file))

        if self.table_frame_name not in C.getFrameNames():
            raise ValueError(f"Table frame '{self.table_frame_name}' not found in scene.")

        if "l_panda_base" not in C.getFrameNames():
            raise ValueError("Frame 'l_panda_base' not found in scene.")

        C.getFrame(self.table_frame_name).setShape(
            ry.ST.ssBox,
            self.table_shape_size,
        )

        C.getFrame("l_panda_base").setRelativePosition(self.panda_base_relative_pos)
        return C

    # =========================================================
    # Geometry
    # =========================================================
    def _quat_from_z_rotation(self, theta: float):
        return [float(np.cos(theta / 2.0)), 0.0, 0.0, float(np.sin(theta / 2.0))]

    def _get_table_info(self, C: ry.Config):
        table = C.getFrame(self.table_frame_name)
        table_pos = np.array(table.getPosition(), dtype=float)
        table_size = np.array(table.getSize(), dtype=float)

        tx, ty, tz = float(table_size[0]), float(table_size[1]), float(table_size[2])
        px, py, pz = float(table_pos[0]), float(table_pos[1]), float(table_pos[2])

        return {
            "frame": table,
            "pos": np.array([px, py, pz], dtype=float),
            "size": np.array([tx, ty, tz], dtype=float),
            "top_z": pz + tz / 2.0,
        }

    def _table_bounds_xy(self, C: ry.Config, margin=0.0):
        info = self._get_table_info(C)
        tx, ty, _ = info["size"]
        px, py, _ = info["pos"]

        xmin = px - tx / 2.0 + margin
        xmax = px + tx / 2.0 - margin
        ymin = py - ty / 2.0 + margin
        ymax = py + ty / 2.0 - margin
        return xmin, xmax, ymin, ymax

    def _quarter_modes(self):
        return ["front_left", "front_right", "back_left", "back_right"]

    def _quarter_bounds_xy(self, C: ry.Config, margin=0.0, quarter_mode=None):
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=margin)
        xmid = 0.5 * (xmin + xmax)
        ymid = 0.5 * (ymin + ymax)

        if quarter_mode == "front_left":
            return xmin, xmid, ymin, ymid
        if quarter_mode == "front_right":
            return xmid, xmax, ymin, ymid
        if quarter_mode == "back_left":
            return xmin, xmid, ymid, ymax
        if quarter_mode == "back_right":
            return xmid, xmax, ymid, ymax

        raise ValueError(f"Unknown quarter_mode: {quarter_mode}")

    def _quarter_center_xy(self, C: ry.Config, quarter_mode):
        xmin, xmax, ymin, ymax = self._quarter_bounds_xy(
            C, margin=0.0, quarter_mode=quarter_mode
        )
        return np.array([(xmin + xmax) * 0.5, (ymin + ymax) * 0.5], dtype=float)

    def _complement_quarters(self, target_quarter):
        return [q for q in self._quarter_modes() if q != target_quarter]

    def _opposite_quarter(self, quarter_mode):
        mapping = {
            "front_left": "back_right",
            "front_right": "back_left",
            "back_left": "front_right",
            "back_right": "front_left",
        }
        if quarter_mode not in mapping:
            raise ValueError(f"Unknown quarter_mode: {quarter_mode}")
        return mapping[quarter_mode]

    def _clutter_region_modes(self):
        if self.target_quarter_mode is None:
            return self._quarter_modes()

        if self.clutter_mode == "high_clutter":
            return [self._opposite_quarter(self.target_quarter_mode)]

        return self._complement_quarters(self.target_quarter_mode)

    def _rotated_xy_aabb_size(self, size_xy, theta: float):
        sx, sy = float(size_xy[0]), float(size_xy[1])
        hx, hy = sx / 2.0, sy / 2.0
        corners = np.array(
            [
                [-hx, -hy],
                [-hx, hy],
                [hx, -hy],
                [hx, hy],
            ],
            dtype=float,
        )

        c = np.cos(theta)
        s = np.sin(theta)
        R = np.array([[c, -s], [s, c]], dtype=float)

        rotated = corners @ R.T
        min_xy = rotated.min(axis=0)
        max_xy = rotated.max(axis=0)
        return min_xy, max_xy, (max_xy - min_xy)

    def _rectangles_overlap(self, rect1, rect2, extra_gap=0.0):
        x1_min, x1_max, y1_min, y1_max = rect1
        x2_min, x2_max, y2_min, y2_max = rect2

        return not (
            x1_max + extra_gap <= x2_min
            or x2_max + extra_gap <= x1_min
            or y1_max + extra_gap <= y2_min
            or y2_max + extra_gap <= y1_min
        )

    def _rect_center(self, rect):
        x_min, x_max, y_min, y_max = rect
        return np.array([(x_min + x_max) * 0.5, (y_min + y_max) * 0.5], dtype=float)

    def _rect_clearance(self, rect1, rect2):
        x1_min, x1_max, y1_min, y1_max = rect1
        x2_min, x2_max, y2_min, y2_max = rect2

        dx = max(0.0, x2_min - x1_max, x1_min - x2_max)
        dy = max(0.0, y2_min - y1_max, y1_min - y2_max)
        return float(np.hypot(dx, dy))

    def _count_overlaps(self, rect, rects, extra_gap=0.0):
        return sum(
            1
            for other in rects
            if self._rectangles_overlap(rect, other, extra_gap=extra_gap)
        )

    # =========================================================
    # Occupancy
    # =========================================================
    def _frame_xy_rect(self, fr):
        try:
            size = np.array(fr.getSize(), dtype=float)
            pos = np.array(fr.getPosition(), dtype=float)
        except Exception:
            return None

        if len(size) < 2 or len(pos) < 2:
            return None

        sx = float(size[0]) if len(size) > 0 else 0.0
        sy = float(size[1]) if len(size) > 1 else sx

        if sx <= 0.0 and sy <= 0.0:
            return None

        x, y = float(pos[0]), float(pos[1])
        return (x - sx / 2.0, x + sx / 2.0, y - sy / 2.0, y + sy / 2.0)

    def _scene_occupied_rects(self, C: ry.Config):
        rects = []
        names = C.getFrameNames()
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=0.0)

        dynamic_prefixes = ("obj_", "goal_", "goal_pose_")

        for nm in names:
            if nm.startswith(dynamic_prefixes):
                continue
            if nm == self.table_frame_name:
                continue

            fr = C.getFrame(nm)
            rect = self._frame_xy_rect(fr)
            if rect is None:
                continue

            rxmin, rxmax, rymin, rymax = rect
            overlaps_table_xy = not (
                rxmax <= xmin or rxmin >= xmax or rymax <= ymin or rymin >= ymax
            )
            if overlaps_table_xy:
                rects.append(rect)

        return rects

    def _current_alive_object_rects(self, C: ry.Config, include_target=False):
        rects = []

        for obj in self.spawned_objects:
            if not obj["alive"]:
                continue
            if (not include_target) and (not obj.get("counts_as_clutter", False)):
                continue

            frame_name = obj["frame_name"]
            if frame_name not in C.getFrameNames():
                continue

            size_xy = obj.get("footprint_size_xy")
            if size_xy is None:
                continue

            fr = C.getFrame(frame_name)
            pos = np.array(fr.getPosition(), dtype=float)
            x = float(pos[0])
            y = float(pos[1])
            half_x = 0.5 * float(size_xy[0])
            half_y = 0.5 * float(size_xy[1])
            rects.append((x - half_x, x + half_x, y - half_y, y + half_y))

        return rects

    def _alive_on_table_objects(self, C: ry.Config, xy_margin=0.02, z_tolerance=0.15):
        alive = [obj for obj in self.spawned_objects if obj["alive"]]
        on_table = [
            obj
            for obj in alive
            if self._is_object_on_table(
                C,
                obj,
                xy_margin=xy_margin,
                z_tolerance=z_tolerance,
            )
        ]
        off_table = [obj for obj in alive if obj not in on_table]
        return on_table, off_table

    # =========================================================
    # Tracking
    # =========================================================
    def _reset_tracking(self):
        self.spawned_objects = []
        self.used_object_names = set()
        self.reserved_object_names = set()
        self.object_counter = 0

        self.target_object = None
        self.target_quarter_mode = None
        self.target_color_name = None
        self.target_rgb = None

        self.goal_clutter_object_prefix = None
        self.goal_pose_object_prefix = None

        self.goal_clutter_insert_index = None
        self.clutter_spawn_success_count = 0
        self.goal_clutter_has_spawned_once = False

    # =========================================================
    # Target selection
    # =========================================================
    def _choose_off_color(self):
        idx = int(self.rng.integers(len(self.OFF_COLOR_PALETTE)))
        color_name, rgb = self.OFF_COLOR_PALETTE[idx]
        return color_name, [float(v) for v in rgb]

    def _choose_target_object(self):
        target_candidates = [
            obj for obj in self.mesh_catalog if obj.get("is_colorable_off_object")
        ]
        if not target_candidates:
            raise RuntimeError(
                "No target candidates found: expected at least one dataset folder "
                "with exactly one .off mesh candidate."
            )

        chosen_idx = int(self.rng.integers(len(target_candidates)))
        target = target_candidates[chosen_idx]
        self.target_color_name, self.target_rgb = self._choose_off_color()
        self.target_object = target
        return target

    def _choose_target_quarter(self):
        quarter = self._quarter_modes()[int(self.rng.integers(4))]
        self.target_quarter_mode = quarter
        return quarter

    def _frame_safe_object_token(self, object_name: str) -> str:
        token = re.sub(r"[^A-Za-z0-9_]+", "_", str(object_name).strip())
        token = re.sub(r"_+", "_", token).strip("_")
        return token or "object"

    def _rgba_to_uint8(self, rgba):
        return np.array(
            [int(round(255.0 * float(v))) for v in rgba],
            dtype=np.uint8,
        )

    def _set_frame_rgba(self, fr, rgba, preserve_existing_rgb=False):
        rgba = [float(v) for v in rgba]

        if hasattr(fr, "setColor"):
            try:
                fr.setColor(rgba)
            except Exception:
                pass

        try:
            attrs = fr.getAttributes()
        except Exception:
            attrs = {}

        if preserve_existing_rgb and "color" in attrs:
            current = list(attrs["color"])
            if len(current) >= 3:
                rgba = [
                    float(current[0]),
                    float(current[1]),
                    float(current[2]),
                    rgba[3],
                ]

        fr.setAttributes({"color": rgba})

    def _set_target_alpha(self, C: ry.Config, frame_name: str, alpha: float):
        if frame_name not in C.getFrameNames():
            return

        fr = C.getFrame(frame_name)
        rgba = [1.0, 1.0, 1.0, float(alpha)]

        try:
            attrs = fr.getAttributes()
            if "color" in attrs:
                current = list(attrs["color"])
                if len(current) >= 3:
                    rgba = [
                        float(current[0]),
                        float(current[1]),
                        float(current[2]),
                        float(alpha),
                    ]
        except Exception:
            pass

        self._set_frame_rgba(fr, rgba, preserve_existing_rgb=True)

    def _goal_pose_rgb_for_frame(self, frame_name: str):
        for obj in self.spawned_objects:
            if obj.get("alive") and obj.get("frame_name") == frame_name:
                rgb = obj.get("rgb")
                if rgb is not None:
                    return [float(v) for v in rgb]

        if self.target_rgb is not None:
            return [float(v) for v in self.target_rgb]

        return [0.0, 1.0, 0.0]

    def _disable_goal_pose_contact(self, C: ry.Config):
        if self.goal_pose_object_prefix is None:
            return

        matching_names = [
            nm for nm in C.getFrameNames() if nm.startswith(self.goal_pose_object_prefix)
        ]

        for nm in matching_names:
            fr = C.getFrame(nm)
            try:
                fr.setContact(0)
            except Exception:
                pass

    def _apply_goal_pose_settled_style(self, C: ry.Config, frame_name: str):
        if frame_name not in C.getFrameNames():
            return

        stale_children = [
            nm for nm in C.getFrameNames()
            if nm.startswith(f"{frame_name}_display")
        ]
        for nm in stale_children:
            if nm in C.getFrameNames():
                C.delFrame(nm)

        fr = C.getFrame(frame_name)
        rgb = self._goal_pose_rgb_for_frame(frame_name)
        rgba = [float(rgb[0]), float(rgb[1]), float(rgb[2]), self.GOAL_POSE_ALPHA]
        pos = np.array(fr.getPosition(), dtype=float)
        quat = np.array(fr.getQuaternion(), dtype=float)
        verts = None
        tris = None

        try:
            verts = fr.getMeshPoints()
            tris = fr.getMeshTriangles()
        except Exception:
            pass

        local_min_z = None
        if self.target_object is not None:
            local_min_z = float(self.target_object["local_aabb_min_after_scaling"][2])

        if local_min_z is not None:
            table_top = self._get_table_info(C)["top_z"]
            pos[2] = float(table_top - local_min_z)

        if verts is not None and tris is not None and len(verts) and len(tris):
            try:
                verts = np.asarray(verts, dtype=float)
                tris = np.asarray(tris, dtype=np.uint32)
                colors = np.tile(
                    self._rgba_to_uint8(rgba),
                    (verts.shape[0], 1),
                )
                C.delFrame(frame_name)
                fr = C.addFrame(frame_name)
                fr.setPosition(pos.tolist())
                fr.setQuaternion(quat.tolist())
                fr.setMesh(verts, tris, colors)
            except Exception:
                pass
        else:
            try:
                fr.setPosition(pos.tolist())
            except Exception:
                pass
            try:
                fr.setQuaternion(quat.tolist())
            except Exception:
                pass

        try:
            fr.setContact(0)
        except Exception:
            pass

        try:
            fr.setMass(0.0)
        except Exception:
            pass

        try:
            fr.setColor(rgba)
        except Exception:
            pass

        try:
            fr.setAttributes({"color": rgba})
        except Exception:
            pass

    def _finalize_goal_pose_state(self, C: ry.Config):
        if self.goal_pose_object_prefix is None:
            return

        matching_names = [
            nm for nm in C.getFrameNames() if nm.startswith(self.goal_pose_object_prefix)
        ]

        for nm in matching_names:
            self._apply_goal_pose_settled_style(C, nm)

    def _compute_goal_clutter_insert_index(self, clutter_total_count: int):
        if clutter_total_count <= 0:
            return None
        return int(round((1.0 - self.hardnessOfTargetObject) * (clutter_total_count - 1)))

    def _has_alive_role(self, role: str):
        return any(
            obj["alive"] and obj.get("role") == role for obj in self.spawned_objects
        )

    def _should_spawn_goal_clutter_now(self):
        if self.target_object is None:
            return False
        if self._has_alive_role("goal"):
            return False
        if self.goal_clutter_has_spawned_once:
            return True
        if self.goal_clutter_insert_index is None:
            return False
        return self.clutter_spawn_success_count >= self.goal_clutter_insert_index

    # =========================================================
    # Placement helpers
    # =========================================================
    def _sample_xy_in_region_bounds(self, C: ry.Config, size_xy, region_mode):
        xmin, xmax, ymin, ymax = self._quarter_bounds_xy(
            C,
            margin=0.0,
            quarter_mode=region_mode,
        )

        half_x = float(size_xy[0]) / 2.0
        half_y = float(size_xy[1]) / 2.0

        x_min = xmin + half_x + self.gap
        x_max = xmax - half_x - self.gap
        y_min = ymin + half_y + self.gap
        y_max = ymax - half_y - self.gap

        if x_min > x_max or y_min > y_max:
            return None

        x = float(self.rng.uniform(x_min, x_max))
        y = float(self.rng.uniform(y_min, y_max))
        rect = (x - half_x, x + half_x, y - half_y, y + half_y)
        return x, y, rect, region_mode

    def _sample_xy_in_regions_bounds(
        self,
        C: ry.Config,
        size_xy,
        region_modes,
        max_tries=256,
    ):
        region_modes = list(region_modes)
        if len(region_modes) == 0:
            raise RuntimeError("No region modes provided for placement.")

        for _ in range(max_tries):
            mode = region_modes[int(self.rng.integers(len(region_modes)))]
            out = self._sample_xy_in_region_bounds(C, size_xy, region_mode=mode)
            if out is not None:
                return out

        for mode in region_modes:
            out = self._sample_xy_in_region_bounds(C, size_xy, region_mode=mode)
            if out is not None:
                return out

        return None

    def _choose_random_clutter_xy(self, C: ry.Config, size_xy, region_modes):
        out = self._sample_xy_in_regions_bounds(
            C,
            size_xy,
            region_modes=region_modes,
            max_tries=256,
        )
        if out is None:
            raise RuntimeError("Could not find in-bounds position in any allowed region.")

        x, y, rect, _ = out
        return x, y, rect

    def _choose_low_clutter_xy(
        self,
        C: ry.Config,
        size_xy,
        occupied_rects,
        region_modes,
    ):
        candidate_count = max(32, self.placement_candidate_count)
        reference_rects = list(occupied_rects)

        best = None
        best_key = None

        for _ in range(candidate_count):
            out = self._sample_xy_in_regions_bounds(
                C,
                size_xy,
                region_modes=region_modes,
                max_tries=16,
            )
            if out is None:
                continue

            x, y, rect, _ = out
            overlap_count = self._count_overlaps(rect, occupied_rects, extra_gap=self.gap)

            if len(reference_rects) > 0:
                min_clearance = min(
                    self._rect_clearance(rect, other) for other in reference_rects
                )
            else:
                min_clearance = float("inf")

            key = (overlap_count, -min_clearance, float(self.rng.random()))
            if best is None or key < best_key:
                best = (x, y, rect)
                best_key = key

        if best is None:
            raise RuntimeError("Could not find any in-bounds low-clutter candidate.")

        return best

    def _choose_high_clutter_xy(
        self,
        C: ry.Config,
        size_xy,
        clutter_rects,
        region_modes,
    ):
        candidate_count = max(32, self.placement_candidate_count)

        if len(clutter_rects) == 0:
            return self._choose_random_clutter_xy(
                C,
                size_xy,
                region_modes=region_modes,
            )

        best = None
        best_key = None

        for _ in range(candidate_count):
            out = self._sample_xy_in_regions_bounds(
                C,
                size_xy,
                region_modes=region_modes,
                max_tries=16,
            )
            if out is None:
                continue

            x, y, rect, _ = out
            rect_center = self._rect_center(rect)

            min_clearance = min(
                self._rect_clearance(rect, other) for other in clutter_rects
            )
            min_center_dist = min(
                float(np.linalg.norm(rect_center - self._rect_center(other)))
                for other in clutter_rects
            )

            key = (min_clearance, min_center_dist, float(self.rng.random()))
            if best is None or key < best_key:
                best = (x, y, rect)
                best_key = key

        if best is None:
            raise RuntimeError("Could not find any in-bounds high-clutter candidate.")

        return best

    def _choose_clutter_xy(
        self,
        C: ry.Config,
        size_xy,
        occupied_rects,
        clutter_rects,
        region_modes,
    ):
        if self.clutter_mode == "random":
            return self._choose_random_clutter_xy(C, size_xy, region_modes=region_modes)
        if self.clutter_mode == "low_clutter":
            return self._choose_low_clutter_xy(
                C,
                size_xy,
                occupied_rects=occupied_rects,
                region_modes=region_modes,
            )
        if self.clutter_mode == "high_clutter":
            return self._choose_high_clutter_xy(
                C,
                size_xy,
                clutter_rects=clutter_rects,
                region_modes=region_modes,
            )
        raise ValueError(f"Unsupported clutter_mode: {self.clutter_mode}")

    def _sample_target_xy_near_quarter_center_no_occupancy_check(
        self,
        C: ry.Config,
        size_xy,
        quarter_mode,
        max_tries=200,
    ):
        xmin, xmax, ymin, ymax = self._quarter_bounds_xy(
            C,
            margin=0.0,
            quarter_mode=quarter_mode,
        )

        half_x = float(size_xy[0]) / 2.0
        half_y = float(size_xy[1]) / 2.0

        x_min = xmin + half_x + self.gap
        x_max = xmax - half_x - self.gap
        y_min = ymin + half_y + self.gap
        y_max = ymax - half_y - self.gap

        if x_min > x_max or y_min > y_max:
            raise RuntimeError(f"Quarter '{quarter_mode}' is too small for target object.")

        center = self._quarter_center_xy(C, quarter_mode)
        usable_width = x_max - x_min
        usable_height = y_max - y_min

        jitter_x = 0.5 * usable_width * self.target_center_jitter_ratio
        jitter_y = 0.5 * usable_height * self.target_center_jitter_ratio

        for _ in range(max_tries):
            x = float(center[0] + self.rng.uniform(-jitter_x, jitter_x))
            y = float(center[1] + self.rng.uniform(-jitter_y, jitter_y))
            x = min(max(x, x_min), x_max)
            y = min(max(y, y_min), y_max)
            rect = (x - half_x, x + half_x, y - half_y, y + half_y)
            return x, y, rect

        raise RuntimeError("Could not sample target XY near quarter center.")

    # =========================================================
    # Spawning
    # =========================================================
    def _spawn_color_metadata(self, mesh_info, object_role: str):
        if not mesh_info.get("is_colorable_off_object"):
            return None, None, None

        if object_role in {"goal", "goal_pose"}:
            if self.target_color_name is None or self.target_rgb is None:
                self.target_color_name, self.target_rgb = self._choose_off_color()
            color_name = str(self.target_color_name)
            rgb = [float(v) for v in self.target_rgb]
        else:
            color_name, rgb = self._choose_off_color()

        alpha = self.GOAL_POSE_ALPHA if object_role == "goal_pose" else 1.0
        rgba = [float(rgb[0]), float(rgb[1]), float(rgb[2]), alpha]
        return color_name, rgb, rgba

    def _spawn_one_mesh(
        self,
        C: ry.Config,
        mesh_info,
        occupied_rects,
        region_modes,
        clutter_rects=None,
        object_role="normal",
        force_quarter_center=False,
        ignore_occupancy_for_target=False,
    ):
        footprint_size_xy = mesh_info["footprint_size_xy"]
        theta = float(self.rng.uniform(0.0, 2.0 * np.pi))
        _, _, rot_size_xy = self._rotated_xy_aabb_size(footprint_size_xy, theta)

        try:
            if object_role == "goal_pose" and force_quarter_center:
                if len(region_modes) != 1:
                    raise ValueError("goal_pose placement expects exactly one quarter.")

                if ignore_occupancy_for_target:
                    x, y, rect = self._sample_target_xy_near_quarter_center_no_occupancy_check(
                        C,
                        rot_size_xy,
                        quarter_mode=region_modes[0],
                    )
                else:
                    raise ValueError("This configuration is not used in current logic.")
            else:
                x, y, rect = self._choose_clutter_xy(
                    C,
                    rot_size_xy,
                    occupied_rects=occupied_rects,
                    clutter_rects=(clutter_rects if clutter_rects is not None else []),
                    region_modes=region_modes,
                )
        except RuntimeError:
            return None

        table_info = self._get_table_info(C)
        local_min_z = float(mesh_info["local_aabb_min_after_scaling"][2])
        z = float(table_info["top_z"] - local_min_z + self.spawn_height)

        prefix_core = f"{self.object_counter}_"
        color_name, rgb, rgba = self._spawn_color_metadata(mesh_info, object_role)
        if object_role == "normal":
            prefix = f"obj_{prefix_core}"
        elif object_role == "goal":
            token_source = (
                f"{color_name}_{mesh_info['object_name']}"
                if color_name is not None
                else mesh_info["object_name"]
            )
            object_token = self._frame_safe_object_token(token_source)
            prefix = f"goal_{object_token}_{prefix_core}"
        elif object_role == "goal_pose":
            token_source = (
                f"{color_name}_{mesh_info['object_name']}"
                if color_name is not None
                else mesh_info["object_name"]
            )
            object_token = self._frame_safe_object_token(token_source)
            prefix = f"goal_pose_{object_token}_{prefix_core}"
        else:
            raise ValueError(f"Unknown object_role: {object_role}")

        frame_name = f"{prefix}mesh"
        self.object_counter += 1

        self._configure_mesh_loading()
        f = C.addFrame(frame_name)
        f.setPosition([x, y, z])
        f.setQuaternion(self._quat_from_z_rotation(theta))
        f.setMeshFile(
            str(mesh_info["load_mesh_path"]),
            scale=float(mesh_info["scale_factor"]),
        )
        if rgba is not None:
            self._set_frame_rgba(f, rgba)
        f.setContact(1)
        f.setMass(float(self.object_mass))

        counts_as_clutter = object_role in {"normal", "goal"}

        obj_info = {
            "prefix": prefix,
            "frame_name": frame_name,
            "object_name": mesh_info["object_name"],
            "mesh_path": str(mesh_info["mesh_path"]),
            "loaded_mesh_path": str(mesh_info["load_mesh_path"]),
            "mesh_basename": mesh_info["mesh_basename"],
            "spawn_xy": (x, y),
            "spawn_z": z,
            "theta_rad": theta,
            "theta_deg": float(np.degrees(theta)),
            "spawn_rect": rect,
            "footprint_size_xy": [float(rot_size_xy[0]), float(rot_size_xy[1])],
            "alive": True,
            "role": object_role,
            "counts_as_clutter": counts_as_clutter,
            "is_target_family": object_role in {"goal", "goal_pose"},
            "target_alpha": rgba[3] if object_role == "goal_pose" and rgba is not None else None,
            "region_modes": list(region_modes),
            "clutter_mode": self.clutter_mode if counts_as_clutter else None,
            "scale_factor": float(mesh_info["scale_factor"]),
            "color_name": color_name,
            "rgb": rgb,
            "rgba": rgba,
            "is_colorable_off_object": bool(mesh_info.get("is_colorable_off_object")),
        }

        self.spawned_objects.append(obj_info)
        self.used_object_names.add(str(mesh_info["object_name"]))

        occupied_rects.append(rect)
        if clutter_rects is not None and counts_as_clutter:
            clutter_rects.append(rect)

        if counts_as_clutter:
            self.clutter_spawn_success_count += 1

        if object_role == "goal":
            self.goal_clutter_object_prefix = prefix
            self.goal_clutter_has_spawned_once = True
        elif object_role == "goal_pose":
            self.goal_pose_object_prefix = prefix

        return obj_info

    def _spawn_goal_clutter_surviving(
        self,
        C: ry.Config,
        sim_seconds,
        sim_dt,
        xy_margin,
        z_tolerance,
        max_spawn_attempts=40,
        verbose=True,
    ):
        if self.target_object is None:
            raise RuntimeError("Target object has not been selected yet.")
        if self.target_quarter_mode is None:
            raise RuntimeError("Target quarter has not been selected yet.")

        clutter_regions = self._clutter_region_modes()
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=xy_margin)
        table_top = self._get_table_info(C)["top_z"]

        if verbose:
            print("\n=== Final goal_ clutter survival check ===")
            print(f"Target object            : {self.target_object['object_name']}")
            print(f"Target mesh path         : {self.target_object['mesh_path']}")
            print(f"Target quarter           : {self.target_quarter_mode}")
            print(f"Allowed clutter regions  : {clutter_regions}")
            print(f"On-table bounds (margin) : x[{xmin:.4f}, {xmax:.4f}] y[{ymin:.4f}, {ymax:.4f}]")
            print(f"Table top z              : {table_top:.4f}")
            print(f"z_tolerance              : {z_tolerance:.4f}")
            print(f"max_spawn_attempts       : {max_spawn_attempts}")

        for attempt_idx in range(1, max_spawn_attempts + 1):
            if verbose:
                print(f"\n--- goal_ attempt {attempt_idx}/{max_spawn_attempts} ---")

            alive_goals = [
                obj for obj in self.spawned_objects if obj["alive"] and obj.get("role") == "goal"
            ]
            alive_goal_on_table = [
                obj
                for obj in alive_goals
                if self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]

            if len(alive_goal_on_table) >= 1:
                keep = alive_goal_on_table[0]
                extras = [obj for obj in alive_goals if obj is not keep]
                if extras:
                    if verbose:
                        print(f"Multiple alive goal_ objects found; removing extras: {len(extras)}")
                    self.remove_objects(C, extras)
                if verbose:
                    print("A surviving on-table goal_ object already exists.")
                return keep

            stale_goals = [obj for obj in alive_goals if obj not in alive_goal_on_table]
            if stale_goals:
                if verbose:
                    print(f"Removing stale/off-table goal_ objects: {len(stale_goals)}")
                self.remove_objects(C, stale_goals)

            static_rects = list(self._scene_occupied_rects(C))
            alive_clutter_rects = self._current_alive_object_rects(C, include_target=False)
            occupied_rects = static_rects + alive_clutter_rects
            clutter_rects = list(alive_clutter_rects)

            goal_obj = self._spawn_one_mesh(
                C,
                self.target_object,
                occupied_rects=occupied_rects,
                clutter_rects=clutter_rects,
                region_modes=clutter_regions,
                object_role="goal",
                force_quarter_center=False,
                ignore_occupancy_for_target=False,
            )

            if goal_obj is None:
                if verbose:
                    print("Spawn failed immediately: _spawn_one_mesh returned None.")
                continue

            frame_name = goal_obj["frame_name"]
            if frame_name not in C.getFrameNames():
                if verbose:
                    print(f"Spawned goal_ frame missing right after spawn: {frame_name}")
                self.remove_objects(C, [goal_obj])
                continue

            fr_before = C.getFrame(frame_name)
            pos_before = np.array(fr_before.getPosition(), dtype=float)
            x0, y0, z0 = float(pos_before[0]), float(pos_before[1]), float(pos_before[2])

            if verbose:
                print(f"Spawn prefix             : {goal_obj['prefix']}")
                print(f"Spawn object             : {goal_obj['object_name']}")
                print(f"Recorded spawn_xy        : {goal_obj['spawn_xy']}")
                print(f"Recorded spawn_z         : {goal_obj['spawn_z']:.4f}")
                print(f"Recorded theta_deg       : {goal_obj['theta_deg']:.2f}")
                print(f"Frame pos before sim     : ({x0:.4f}, {y0:.4f}, {z0:.4f})")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            if frame_name not in C.getFrameNames():
                if verbose:
                    print("goal_ disappeared from config after simulation.")
                self.remove_objects(C, [goal_obj])
                continue

            fr_after = C.getFrame(frame_name)
            pos_after = np.array(fr_after.getPosition(), dtype=float)
            x1, y1, z1 = float(pos_after[0]), float(pos_after[1]), float(pos_after[2])

            inside_xy = (xmin <= x1 <= xmax) and (ymin <= y1 <= ymax)
            not_too_low = z1 >= (table_top - z_tolerance)
            survived = inside_xy and not_too_low

            if verbose:
                print(f"Frame pos after sim      : ({x1:.4f}, {y1:.4f}, {z1:.4f})")
                print(f"Inside XY bounds?        : {inside_xy}")
                print(f"Above z threshold?       : {not_too_low}")

            if survived:
                if verbose:
                    print("Result                   : SUCCESS (goal_ survived on table)")
                return goal_obj

            if verbose:
                print("Result                   : FAILED -> removing goal_ and retrying")

            self.remove_objects(C, [goal_obj])

        raise RuntimeError("Failed to obtain a surviving on-table goal_ clutter object.")

    def _spawn_target_mesh_surviving(
        self,
        C: ry.Config,
        sim_seconds,
        sim_dt,
        xy_margin,
        z_tolerance,
        max_spawn_attempts=40,
        verbose=True,
    ):
        if self.target_object is None:
            raise RuntimeError("Target object has not been selected yet.")
        if self.target_quarter_mode is None:
            raise RuntimeError("Target quarter has not been selected yet.")

        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=xy_margin)
        table_top = self._get_table_info(C)["top_z"]

        qxmin, qxmax, qymin, qymax = self._quarter_bounds_xy(
            C,
            margin=0.0,
            quarter_mode=self.target_quarter_mode,
        )

        if verbose:
            print("\n=== goal_pose spawn diagnostics ===")
            print(f"Target object            : {self.target_object['object_name']}")
            print(f"Target quarter           : {self.target_quarter_mode}")
            print(f"Target quarter bounds    : x[{qxmin:.4f}, {qxmax:.4f}] y[{qymin:.4f}, {qymax:.4f}]")
            print(f"On-table bounds (margin) : x[{xmin:.4f}, {xmax:.4f}] y[{ymin:.4f}, {ymax:.4f}]")
            print(f"Table top z              : {table_top:.4f}")
            print(f"z_tolerance              : {z_tolerance:.4f}")
            print(f"sim_seconds              : {sim_seconds}")
            print(f"sim_dt                   : {sim_dt}")
            print(f"max_spawn_attempts       : {max_spawn_attempts}")

        for attempt_idx in range(1, max_spawn_attempts + 1):
            if verbose:
                print(f"\n--- goal_pose attempt {attempt_idx}/{max_spawn_attempts} ---")

            static_rects = list(self._scene_occupied_rects(C))
            target_obj = self._spawn_one_mesh(
                C,
                self.target_object,
                occupied_rects=static_rects,
                clutter_rects=[],
                region_modes=[self.target_quarter_mode],
                object_role="goal_pose",
                force_quarter_center=False,
                ignore_occupancy_for_target=False,
            )

            if target_obj is None:
                if verbose:
                    print("Spawn failed immediately: _spawn_one_mesh returned None.")
                continue

            frame_name = target_obj["frame_name"]
            if frame_name not in C.getFrameNames():
                if verbose:
                    print(f"Spawned goal_pose frame missing right after spawn: {frame_name}")
                self.remove_objects(C, [target_obj])
                continue

            fr_before = C.getFrame(frame_name)
            pos_before = np.array(fr_before.getPosition(), dtype=float)
            x0, y0, z0 = float(pos_before[0]), float(pos_before[1]), float(pos_before[2])

            if verbose:
                print(f"Spawn prefix             : {target_obj['prefix']}")
                print(f"Spawn object             : {target_obj['object_name']}")
                print(f"Recorded spawn_xy        : {target_obj['spawn_xy']}")
                print(f"Recorded spawn_z         : {target_obj['spawn_z']:.4f}")
                print(f"Recorded theta_deg       : {target_obj['theta_deg']:.2f}")
                print(f"Frame pos before sim     : ({x0:.4f}, {y0:.4f}, {z0:.4f})")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            if frame_name not in C.getFrameNames():
                if verbose:
                    print("goal_pose disappeared from config after simulation.")
                self.remove_objects(C, [target_obj])
                continue

            fr_after = C.getFrame(frame_name)
            pos_after = np.array(fr_after.getPosition(), dtype=float)
            x1, y1, z1 = float(pos_after[0]), float(pos_after[1]), float(pos_after[2])

            inside_xy = (xmin <= x1 <= xmax) and (ymin <= y1 <= ymax)
            not_too_low = z1 >= (table_top - z_tolerance)
            survived = inside_xy and not_too_low

            if verbose:
                print(f"Frame pos after sim      : ({x1:.4f}, {y1:.4f}, {z1:.4f})")
                print(f"Inside XY bounds?        : {inside_xy}")
                print(f"Above z threshold?       : {not_too_low}")

            if survived:
                rgb = target_obj.get("rgb") or self.target_rgb or [0.0, 1.0, 0.0]
                target_obj["target_alpha"] = self.GOAL_POSE_ALPHA
                target_obj["final_rgba"] = [
                    float(rgb[0]),
                    float(rgb[1]),
                    float(rgb[2]),
                    self.GOAL_POSE_ALPHA,
                ]
                if verbose:
                    print("Result                   : SUCCESS (goal_pose survived on table)")
                    print("Finalized goal_pose      : pending final settled-frame styling")
                return target_obj

            if verbose:
                print("Result                   : FAILED -> removing goal_pose and retrying")

            self.remove_objects(C, [target_obj])

        raise RuntimeError("Failed to spawn a goal_pose object that survives on the table.")

    def spawn_objects_best_effort(self, C: ry.Config, target_count):
        static_rects = list(self._scene_occupied_rects(C))
        alive_clutter_rects = self._current_alive_object_rects(C, include_target=False)

        occupied_rects = static_rects + alive_clutter_rects
        clutter_rects = list(alive_clutter_rects)

        usable_objects = [
            obj
            for obj in self.mesh_catalog
            if obj["object_name"] not in self.reserved_object_names
        ]

        unused_objects = [
            obj for obj in usable_objects if obj["object_name"] not in self.used_object_names
        ]
        already_used_objects = [
            obj for obj in usable_objects if obj["object_name"] in self.used_object_names
        ]
        candidate_objects = list(unused_objects) + list(already_used_objects)
        self.rng.shuffle(candidate_objects)

        spawned = []
        attempted_object_names = set()
        clutter_regions = self._clutter_region_modes()

        while len(spawned) < target_count:
            found_one = False

            if self._should_spawn_goal_clutter_now():
                goal_obj = self._spawn_one_mesh(
                    C,
                    self.target_object,
                    occupied_rects=occupied_rects,
                    clutter_rects=clutter_rects,
                    region_modes=clutter_regions,
                    object_role="goal",
                    force_quarter_center=False,
                    ignore_occupancy_for_target=False,
                )
                if goal_obj is not None:
                    spawned.append(goal_obj)
                    found_one = True
                    continue
                break

            for mesh_info in candidate_objects:
                object_name = mesh_info["object_name"]
                if object_name in attempted_object_names:
                    continue

                obj = self._spawn_one_mesh(
                    C,
                    mesh_info,
                    occupied_rects=occupied_rects,
                    clutter_rects=clutter_rects,
                    region_modes=clutter_regions,
                    object_role="normal",
                    force_quarter_center=False,
                    ignore_occupancy_for_target=False,
                )
                attempted_object_names.add(object_name)

                if obj is not None:
                    spawned.append(obj)
                    found_one = True
                    break

            if not found_one:
                break

        return spawned

    # =========================================================
    # Simulation
    # =========================================================
    def run_physx(self, C: ry.Config, sim_seconds=7.0, sim_dt=0.01):
        S = ry.Simulation(C, ry.SimulationEngine.physx, verbose=0)
        S.pushConfigToSim()

        steps = int(np.ceil(sim_seconds / sim_dt))
        for _ in range(steps):
            S.step([], sim_dt, ry.ControlMode.none)

        try:
            state = S.getState()
            free_frames = [fr.name for fr in S.getFreeFrames()]

            if free_frames and getattr(state, "freePos", None) is not None:
                C.setFrameState(state.freePos, free_frames)

            if getattr(state, "q", None) is not None:
                q = np.asarray(state.q, dtype=float)
                if q.size:
                    C.setJointState(q)
        except Exception:
            pass

        del S

    # =========================================================
    # Object validity
    # =========================================================
    def _is_object_on_table(self, C: ry.Config, obj, xy_margin=0.01, z_tolerance=0.15):
        frame_name = obj["frame_name"]
        if frame_name not in C.getFrameNames():
            return False

        fr = C.getFrame(frame_name)
        pos = np.array(fr.getPosition(), dtype=float)
        x, y, z = pos

        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=xy_margin)
        table_top = self._get_table_info(C)["top_z"]

        inside_xy = (xmin <= x <= xmax) and (ymin <= y <= ymax)
        not_too_low = z >= (table_top - z_tolerance)
        return inside_xy and not_too_low

    def find_objects_off_table(self, C: ry.Config, xy_margin=0.01, z_tolerance=0.15):
        off_table = []
        on_table = []

        for obj in self.spawned_objects:
            if not obj["alive"]:
                continue
            if self._is_object_on_table(
                C,
                obj,
                xy_margin=xy_margin,
                z_tolerance=z_tolerance,
            ):
                on_table.append(obj)
            else:
                off_table.append(obj)

        return on_table, off_table

    def remove_objects(self, C: ry.Config, objects_to_remove):
        frame_names = set(C.getFrameNames())

        for obj in objects_to_remove:
            prefix = obj["prefix"]
            matching = [nm for nm in frame_names if nm.startswith(prefix)]

            for nm in sorted(matching, reverse=True):
                if nm in C.getFrameNames():
                    C.delFrame(nm)

            obj["alive"] = False

    # =========================================================
    # Main generation
    # =========================================================
    def _resolve_num_objects(self, num_objects, num_voxels):
        if num_objects is not None and num_voxels is not None:
            raise ValueError("Provide either num_objects or num_voxels, not both.")
        if num_objects is not None:
            return int(num_objects)
        if num_voxels is not None:
            return int(num_voxels)
        return 15

    def create_environment_with_refill(
        self,
        num_objects=None,
        *,
        num_voxels=None,
        sim_seconds=7.0,
        sim_dt=0.01,
        max_refill_rounds=10,
        xy_margin=0.02,
        z_tolerance=0.15,
        batch_spawn_count=5,
        max_target_spawn_attempts=40,
    ):
        num_objects = self._resolve_num_objects(num_objects, num_voxels)

        C = self._load_base_scene()
        self._reset_tracking()

        if num_objects <= 0:
            summary = {
                "target": num_objects,
                "final_on_table": 0,
                "final_off_table": 0,
                "rounds": 0,
                "batch_spawn_count": batch_spawn_count,
                "clutter_mode": self.clutter_mode,
                "objects": self.spawned_objects,
                "target_object_name": None,
                "target_mesh_path": None,
                "target_mesh_basename": None,
                "target_quarter_mode": None,
                "goal_clutter_object_prefix": None,
                "goal_pose_object_prefix": None,
                "target_color_name": None,
                "target_rgb": None,
                "target_alpha": self.target_alpha,
                "hardnessOfTargetObject": self.hardnessOfTargetObject,
                "goal_clutter_insert_index": None,
            }
            return C, summary

        target_object = self._choose_target_object()
        target_quarter = self._choose_target_quarter()
        self.reserved_object_names.add(target_object["object_name"])

        clutter_target_count = int(num_objects)
        self.goal_clutter_insert_index = self._compute_goal_clutter_insert_index(
            clutter_target_count
        )

        print("Chosen target object:", target_object["object_name"])
        print("Chosen target mesh:", target_object["mesh_basename"])
        print("Chosen target color:", self.target_color_name, self.target_rgb)
        print("Chosen target quarter:", target_quarter)
        print("Clutter mode:", self.clutter_mode)
        print("hardnessOfTargetObject:", self.hardnessOfTargetObject)
        print("goal_ clutter insert index:", self.goal_clutter_insert_index)

        if self.clutter_mode == "high_clutter":
            print("Opposite clutter quarter:", self._opposite_quarter(target_quarter))

        initial_spawn_count = min(batch_spawn_count, clutter_target_count)
        initially_spawned = self.spawn_objects_best_effort(C, initial_spawn_count)
        print(
            f"Initially spawned clutter objects: "
            f"{len(initially_spawned)} / {initial_spawn_count}"
        )

        round_idx = 0
        while True:
            round_idx += 1
            print(f"\n=== Clutter simulation round {round_idx} ===")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            alive_clutter = [
                obj
                for obj in self.spawned_objects
                if obj["alive"] and obj.get("counts_as_clutter", False)
            ]
            off_clutter = [
                obj
                for obj in alive_clutter
                if not self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]
            on_clutter = [
                obj
                for obj in alive_clutter
                if self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]

            goal_on = [obj for obj in on_clutter if obj.get("role") == "goal"]
            dynamic_clutter_target = clutter_target_count + (0 if len(goal_on) == 1 else 1)

            print(
                f"Clutter on table: {len(on_clutter)} | "
                f"Off table: {len(off_clutter)} | "
                f"Base clutter target: {clutter_target_count} | "
                f"Dynamic clutter target: {dynamic_clutter_target} | "
                f"goal_ on table: {len(goal_on)}"
            )

            if len(on_clutter) >= clutter_target_count and len(goal_on) == 1:
                print("Desired clutter count is on the table, including a surviving goal_ target.")
                break

            if round_idx >= max_refill_rounds:
                print("Reached max refill rounds for clutter.")
                break

            if off_clutter:
                self.remove_objects(C, off_clutter)

            alive_clutter_after_removal = [
                obj
                for obj in self.spawned_objects
                if obj["alive"] and obj.get("counts_as_clutter", False)
            ]
            on_clutter_after_removal = [
                obj
                for obj in alive_clutter_after_removal
                if self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]
            goal_on_after_removal = [
                obj for obj in on_clutter_after_removal if obj.get("role") == "goal"
            ]

            dynamic_clutter_target_after_removal = clutter_target_count + (
                0 if len(goal_on_after_removal) == 1 else 1
            )

            missing = dynamic_clutter_target_after_removal - len(on_clutter_after_removal)
            to_spawn_now = min(batch_spawn_count, max(0, missing))

            print(
                f"Trying to respawn up to {to_spawn_now} clutter object(s)... "
                f"(goal present on table? {'yes' if len(goal_on_after_removal) == 1 else 'no'})"
            )

            spawned_now = self.spawn_objects_best_effort(C, to_spawn_now)
            print(f"Respawned {len(spawned_now)} clutter object(s).")

            if len(spawned_now) == 0:
                print("Could not spawn any new clutter object this round. Stopping clutter refill.")
                break

        alive_clutter = [
            obj
            for obj in self.spawned_objects
            if obj["alive"] and obj.get("counts_as_clutter", False)
        ]
        final_off_clutter = [
            obj
            for obj in alive_clutter
            if not self._is_object_on_table(
                C,
                obj,
                xy_margin=xy_margin,
                z_tolerance=z_tolerance,
            )
        ]
        if final_off_clutter:
            print(f"Removing {len(final_off_clutter)} final off-table clutter object(s).")
            self.remove_objects(C, final_off_clutter)

        print("\n=== Final rescue check for goal_ ===")
        goal_obj = self._spawn_goal_clutter_surviving(
            C,
            sim_seconds=sim_seconds,
            sim_dt=sim_dt,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
            max_spawn_attempts=max_target_spawn_attempts,
        )
        print(f"Confirmed surviving goal_ object: {goal_obj['object_name']}")

        print("\n=== Spawning goal_pose last ===")
        goal_pose_obj = self._spawn_target_mesh_surviving(
            C,
            sim_seconds=sim_seconds,
            sim_dt=sim_dt,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
            max_spawn_attempts=max_target_spawn_attempts,
        )
        print(f"Spawned surviving goal_pose object: {goal_pose_obj['object_name']}")

        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        if final_off:
            final_off_non_pose = [obj for obj in final_off if obj.get("role") != "goal_pose"]
            if final_off_non_pose:
                print(
                    f"Removing {len(final_off_non_pose)} final off-table non-goal_pose object(s)."
                )
                self.remove_objects(C, final_off_non_pose)

        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        alive_goal = [obj for obj in final_on if obj.get("role") == "goal"]
        alive_goal_pose = [obj for obj in final_on if obj.get("role") == "goal_pose"]

        if len(alive_goal) != 1:
            raise RuntimeError(
                "Final scene does not contain exactly one surviving on-table goal_ clutter object."
            )
        if len(alive_goal_pose) != 1:
            raise RuntimeError(
                "Final scene does not contain exactly one surviving on-table goal_pose_ object."
            )

        self._apply_goal_pose_settled_style(C, alive_goal_pose[0]["frame_name"])
        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        summary = {
            "target": num_objects,
            "final_on_table": len(final_on),
            "final_off_table": len(final_off),
            "rounds": round_idx,
            "batch_spawn_count": batch_spawn_count,
            "clutter_mode": self.clutter_mode,
            "objects": self.spawned_objects,
            "target_object_name": self.target_object["object_name"] if self.target_object else None,
            "target_mesh_path": (
                str(self.target_object["mesh_path"]) if self.target_object else None
            ),
            "target_mesh_basename": (
                self.target_object["mesh_basename"] if self.target_object else None
            ),
            "goal_clutter_mesh_basename": (
                f"goal_{self.target_object['mesh_basename']}" if self.target_object else None
            ),
            "goal_pose_mesh_basename": (
                f"goal_pose_{self.target_object['mesh_basename']}"
                if self.target_object
                else None
            ),
            "target_quarter_mode": self.target_quarter_mode,
            "goal_clutter_object_prefix": self.goal_clutter_object_prefix,
            "goal_pose_object_prefix": self.goal_pose_object_prefix,
            "target_color_name": self.target_color_name,
            "target_rgb": self.target_rgb,
            "target_alpha": self.GOAL_POSE_ALPHA,
            "hardnessOfTargetObject": self.hardnessOfTargetObject,
            "goal_clutter_insert_index": self.goal_clutter_insert_index,
        }

        return C, summary

    # =========================================================
    # Save / reload
    # =========================================================
    def _restore_goal_pose_mesh_metadata(self, scene_text: str, out_dir: Path) -> str:
        goal_pose_objs = [
            obj
            for obj in self.spawned_objects
            if obj["alive"] and obj.get("role") == "goal_pose"
        ]
        if len(goal_pose_objs) != 1:
            return scene_text

        obj = goal_pose_objs[0]
        frame_name = str(obj["frame_name"])
        mesh_path = self._norm_path(obj["mesh_path"])
        save_mesh_path = Path(
            os.path.relpath(mesh_path, start=out_dir)
        ).as_posix()
        scale_factor = float(obj["scale_factor"])

        line_re = re.compile(
            rf"(^\s*{re.escape(frame_name)}(?:\([^)]*\))?\s*:\s*\{{)(.*?)(\}}\s*$)",
            re.MULTILINE,
        )

        def _patch(match: re.Match[str]) -> str:
            prefix, body, suffix = match.groups()
            body = body.strip()

            body = re.sub(r"\bmass\s*:\s*(?:\[[^\]]*\]|[^\s,}]+)", "mass: 0.0", body)

            extras = []
            if "mesh:" not in body:
                extras.append(f"mesh: <{save_mesh_path}>")
            if "meshscale:" not in body:
                extras.append(f"meshscale: [{scale_factor:.8g}]")
            if "contact:" not in body:
                extras.append("contact: 0")
            if "mass:" not in body:
                extras.append("mass: 0.0")

            if not extras:
                return match.group(0)

            if body:
                body = f"{body}, " + ", ".join(extras)
            else:
                body = ", ".join(extras)
            return f"{prefix} {body} {suffix}"

        return line_re.sub(_patch, scene_text, count=1)

    def _scene_text_with_saved_mesh_paths(self, C: ry.Config, out_file: Path):
        scene_text = C.write()
        out_dir = out_file.parent.resolve(strict=False)

        for obj in self.spawned_objects:
            if not obj["alive"]:
                continue

            loaded_mesh_path = str(obj.get("loaded_mesh_path", obj["mesh_path"]))
            mesh_path = self._norm_path(obj["mesh_path"])
            save_mesh_path = Path(
                os.path.relpath(mesh_path, start=out_dir)
            ).as_posix()

            scene_text = scene_text.replace(loaded_mesh_path, save_mesh_path)
            scene_text = scene_text.replace(str(mesh_path), save_mesh_path)

        scene_text = self._restore_goal_pose_mesh_metadata(scene_text, out_dir)
        return _sanitize_scene_text_for_addfile(scene_text)

    def save_environment(self, C: ry.Config, file_name="generated_panda_table_mesh_clutter.g"):
        self._finalize_goal_pose_state(C)
        out_file = self.output_dir / file_name
        return save_config_as_g(
            C,
            out_file,
            spawned_objects=self.spawned_objects,
        )

    def reload_saved_environment(
        self,
        scene_file,
        cache_bust_mesh_paths=True,
        cache_root=None,
    ):
        return recreate_scene_from_g(
            scene_file=scene_file,
            cache_bust_mesh_paths=cache_bust_mesh_paths,
            cache_root=cache_root,
        )
