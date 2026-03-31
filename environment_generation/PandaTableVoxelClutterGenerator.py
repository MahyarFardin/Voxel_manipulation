import os
from glob import glob
from pathlib import Path

import numpy as np
import robotic as ry


class PandaTableVoxelClutterGenerator:
    """
    Generates Panda-table voxel scenes with these rules:

    1. One target voxel is chosen in advance.
    2. One random table quarter is assigned to that target.
    3. All non-target voxels are spawned only in the other three quarters.
    4. Non-target voxels are simulated/refilled first.
    5. The target is spawned last.
    6. The target is spawned near the center of its assigned quarter.
    7. The target quarter is NOT checked for emptiness during target insertion.
    8. The target must survive simulation and remain on the table.
    9. The target is loaded with a frame prefix starting with 'goal_'.
    10. The alpha channel of all target cubes is changed while preserving RGB.

    Non-target clutter placement modes:
    - "random": purely random inside the 3 allowed quarters, no clutter overlap check
    - "low_clutter": best-effort spread-out placement, prefers non-collision and open areas
    - "high_clutter": prefers placement close to existing clutter, creating dense clusters
    """

    def __init__(
        self,
        base_scene_file=ry.raiPath("../rai-robotModels/scenarios/pandaSingle.g"),
        voxel_dir="../voxel_generation/data/voxels",
        output_dir="./generated_envs",
        table_frame_name="table",
        gap=0.04,
        spawn_height=0.41,
        seed=15,
        per_cube_mass=0.2,
        table_shape_size=(1.6, 1.6, 0.08, 0.02),
        panda_base_relative_pos=(0.0, 0.0, 0.05),
        target_alpha=0.35,
        target_center_jitter_ratio=0.10,
        clutter_mode="random",
        placement_candidate_count=96,
    ):
        self.base_scene_file = Path(base_scene_file)
        self.voxel_dir = Path(voxel_dir)
        self.output_dir = Path(output_dir)
        self.table_frame_name = table_frame_name
        self.gap = float(gap)
        self.spawn_height = float(spawn_height)
        self.seed = seed
        self.per_cube_mass = float(per_cube_mass)
        self.table_shape_size = list(table_shape_size)
        self.panda_base_relative_pos = list(panda_base_relative_pos)
        self.target_alpha = float(target_alpha)
        self.target_center_jitter_ratio = float(target_center_jitter_ratio)

        self.clutter_mode = str(clutter_mode)
        self.placement_candidate_count = int(placement_candidate_count)

        allowed_modes = {"random", "low_clutter", "high_clutter"}
        if self.clutter_mode not in allowed_modes:
            raise ValueError(
                f"Unknown clutter_mode: {self.clutter_mode}. "
                f"Allowed: {sorted(allowed_modes)}"
            )

        if not self.base_scene_file.exists():
            raise FileNotFoundError(f"Base scene file not found: {self.base_scene_file}")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rng = np.random.default_rng(self.seed)

        self.spawned_objects = []
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0

        self.target_voxel_file = None
        self.target_quarter_mode = None
        self.target_object_prefix = None

    # =========================================================
    # Basic helpers
    # =========================================================
    def _cube_frames(self, C: ry.Config, prefix: str):
        return [n for n in C.getFrameNames() if n.startswith(prefix) and "cube" in n]

    def _quat_from_z_rotation(self, theta: float):
        return [float(np.cos(theta / 2.0)), 0.0, 0.0, float(np.sin(theta / 2.0))]

    def _load_voxel_files(self):
        voxel_files = sorted(glob(str(self.voxel_dir / "*.g")))
        if not voxel_files:
            raise FileNotFoundError(f"No voxel files found in: {self.voxel_dir}")
        return voxel_files

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

        C.getFrame("l_panda_base").setRelativePosition(
            self.panda_base_relative_pos
        )

        return C

    # =========================================================
    # Geometry
    # =========================================================
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

    # =========================================================
    # Voxel geometry
    # =========================================================
    def _voxel_cube_geometry(self, file_path: str):
        T = ry.Config()
        T.addFile(file_path, namePrefix="tmp_")

        cube_names = self._cube_frames(T, "tmp_")
        if len(cube_names) == 0:
            raise ValueError(f"No cube frames found in {file_path}")

        cubes = []
        for nm in cube_names:
            fr = T.getFrame(nm)

            size = np.array(fr.getSize()[:3], dtype=float)
            pos = np.array(fr.getPosition(), dtype=float)

            color = [0.8, 0.8, 0.8]
            try:
                attrs = fr.getAttributes()
                if "color" in attrs:
                    raw_color = list(attrs["color"])
                    if len(raw_color) >= 3:
                        color = [
                            float(raw_color[0]),
                            float(raw_color[1]),
                            float(raw_color[2]),
                        ]
            except Exception:
                pass

            cubes.append({
                "name": nm,
                "pos": pos,
                "size": size,
                "color": color,
            })

        return cubes

    def _local_aabb(self, cubes):
        min_corner = np.array([np.inf, np.inf, np.inf], dtype=float)
        max_corner = np.array([-np.inf, -np.inf, -np.inf], dtype=float)

        for cube in cubes:
            pos = cube["pos"]
            half = cube["size"] / 2.0
            min_corner = np.minimum(min_corner, pos - half)
            max_corner = np.maximum(max_corner, pos + half)

        return min_corner, max_corner

    def _rotated_xy_aabb_size(self, cubes, theta: float):
        c = np.cos(theta)
        s = np.sin(theta)
        R = np.array([[c, -s], [s, c]], dtype=float)

        min_xy = np.array([np.inf, np.inf], dtype=float)
        max_xy = np.array([-np.inf, -np.inf], dtype=float)

        for cube in cubes:
            center_xy = cube["pos"][:2]
            sx, sy = cube["size"][:2]
            hx, hy = sx / 2.0, sy / 2.0

            corners = np.array([
                [center_xy[0] - hx, center_xy[1] - hy],
                [center_xy[0] - hx, center_xy[1] + hy],
                [center_xy[0] + hx, center_xy[1] - hy],
                [center_xy[0] + hx, center_xy[1] + hy],
            ])

            rotated = corners @ R.T
            min_xy = np.minimum(min_xy, rotated.min(axis=0))
            max_xy = np.maximum(max_xy, rotated.max(axis=0))

        return min_xy, max_xy, (max_xy - min_xy)

    def _rectangles_overlap(self, rect1, rect2, extra_gap=0.0):
        x1_min, x1_max, y1_min, y1_max = rect1
        x2_min, x2_max, y2_min, y2_max = rect2

        return not (
            x1_max + extra_gap <= x2_min or
            x2_max + extra_gap <= x1_min or
            y1_max + extra_gap <= y2_min or
            y2_max + extra_gap <= y1_min
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
            1 for other in rects
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

        for nm in names:
            if nm.startswith("obj") or nm.startswith("goal_obj"):
                continue
            if nm == self.table_frame_name:
                continue

            fr = C.getFrame(nm)
            rect = self._frame_xy_rect(fr)
            if rect is None:
                continue

            rxmin, rxmax, rymin, rymax = rect
            overlaps_table_xy = not (
                rxmax <= xmin or rxmin >= xmax or
                rymax <= ymin or rymin >= ymax
            )
            if overlaps_table_xy:
                rects.append(rect)

        return rects

    def _current_alive_object_rects(self, C: ry.Config, include_target=False):
        rects = []

        for obj in self.spawned_objects:
            if not obj["alive"]:
                continue
            if obj.get("is_target", False) and not include_target:
                continue

            base_name = f"{obj['prefix']}base"
            if base_name not in C.getFrameNames():
                continue

            size_xy = obj.get("footprint_size_xy", None)
            if size_xy is None:
                continue

            base = C.getFrame(base_name)
            pos = np.array(base.getPosition(), dtype=float)
            x = float(pos[0])
            y = float(pos[1])

            half_x = 0.5 * float(size_xy[0])
            half_y = 0.5 * float(size_xy[1])

            rect = (x - half_x, x + half_x, y - half_y, y + half_y)
            rects.append(rect)

        return rects

    # =========================================================
    # Tracking
    # =========================================================
    def _reset_tracking(self):
        self.spawned_objects = []
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0
        self.target_voxel_file = None
        self.target_quarter_mode = None
        self.target_object_prefix = None

    # =========================================================
    # Target selection
    # =========================================================
    def _choose_target_voxel(self):
        voxel_files = self._load_voxel_files()
        chosen_idx = int(self.rng.integers(len(voxel_files)))
        voxel_file = str(voxel_files[chosen_idx])
        self.target_voxel_file = voxel_file
        return voxel_file

    def _choose_target_quarter(self):
        quarter = self._quarter_modes()[int(self.rng.integers(4))]
        self.target_quarter_mode = quarter
        return quarter

    def _set_target_alpha(self, C: ry.Config, prefix: str, alpha: float):
        cube_names = self._cube_frames(C, prefix)

        for nm in cube_names:
            fr = C.getFrame(nm)

            rgb = [0.8, 0.8, 0.8]
            try:
                attrs = fr.getAttributes()
                if "color" in attrs:
                    raw_color = list(attrs["color"])
                    if len(raw_color) >= 3:
                        rgb = [
                            float(raw_color[0]),
                            float(raw_color[1]),
                            float(raw_color[2]),
                        ]
            except Exception:
                pass

            fr.setAttributes({"color": [rgb[0], rgb[1], rgb[2], float(alpha)]})

    # =========================================================
    # Placement helpers
    # =========================================================
    def _sample_xy_in_region_bounds(
        self,
        C: ry.Config,
        size_xy,
        region_mode,
    ):
        xmin, xmax, ymin, ymax = self._quarter_bounds_xy(
            C,
            margin=0.0,
            quarter_mode=region_mode,
        )

        half_x = size_xy[0] / 2.0
        half_y = size_xy[1] / 2.0

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
            out = self._sample_xy_in_region_bounds(
                C,
                size_xy,
                region_mode=mode,
            )
            if out is not None:
                return out

        for mode in region_modes:
            out = self._sample_xy_in_region_bounds(
                C,
                size_xy,
                region_mode=mode,
            )
            if out is not None:
                return out

        return None

    def _choose_random_clutter_xy(
        self,
        C: ry.Config,
        size_xy,
        region_modes,
    ):
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

            overlap_count = self._count_overlaps(
                rect,
                occupied_rects,
                extra_gap=self.gap,
            )

            if len(reference_rects) > 0:
                min_clearance = min(
                    self._rect_clearance(rect, other) for other in reference_rects
                )
            else:
                min_clearance = float("inf")

            random_tiebreak = float(self.rng.random())

            # Primary goal: minimize overlap count (with gap).
            # Secondary goal: maximize nearest clearance.
            key = (overlap_count, -min_clearance, random_tiebreak)

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

            random_tiebreak = float(self.rng.random())

            # Prefer candidates close to existing clutter.
            key = (min_clearance, min_center_dist, random_tiebreak)

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
            return self._choose_random_clutter_xy(
                C,
                size_xy,
                region_modes=region_modes,
            )

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

        half_x = size_xy[0] / 2.0
        half_y = size_xy[1] / 2.0

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
    def _spawn_one_voxel(
        self,
        C: ry.Config,
        gfile: str,
        occupied_rects,
        region_modes,
        clutter_rects=None,
        is_target=False,
        force_quarter_center=False,
        ignore_occupancy_for_target=False,
    ):
        cubes = self._voxel_cube_geometry(gfile)
        local_min, _ = self._local_aabb(cubes)

        theta = float(self.rng.uniform(0.0, 2.0 * np.pi))
        _, _, rot_size_xy = self._rotated_xy_aabb_size(cubes, theta)

        try:
            if is_target and force_quarter_center:
                if len(region_modes) != 1:
                    raise ValueError("Target center placement expects exactly one quarter.")

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
        z = float(table_info["top_z"] - local_min[2] + self.spawn_height)

        prefix_core = f"{self.object_counter}_"
        prefix = f"goal_obj{prefix_core}" if is_target else f"obj{prefix_core}"
        self.object_counter += 1

        C.addFile(gfile, namePrefix=prefix)

        base = C.getFrame(f"{prefix}base")
        base.setAttributes({
            "multibody": True,
            "multibody_fixedBase": False,
            "multibody_gravity": True,
        })
        base.setPosition([x, y, z])
        base.setQuaternion(self._quat_from_z_rotation(theta))

        voxel_names = self._cube_frames(C, prefix)

        for nm in voxel_names:
            fr = C.getFrame(nm)
            fr.setContact(True)
            fr.setMass(self.per_cube_mass)

        if is_target:
            self._set_target_alpha(C, prefix, self.target_alpha)

            voxel_names = self._cube_frames(C, prefix)
            for nm in voxel_names:
                fr = C.getFrame(nm)
                fr.setContact(True)
                fr.setMass(self.per_cube_mass)

            self.target_object_prefix = prefix

        basename = os.path.basename(gfile)
        reported_basename = f"goal_{basename}" if is_target else basename

        obj_info = {
            "prefix": prefix,
            "file": str(gfile),
            "basename": reported_basename,
            "original_basename": basename,
            "spawn_xy": (x, y),
            "spawn_z": z,
            "theta_rad": theta,
            "theta_deg": float(np.degrees(theta)),
            "spawn_rect": rect,
            "footprint_size_xy": [float(rot_size_xy[0]), float(rot_size_xy[1])],
            "alive": True,
            "is_target": bool(is_target),
            "target_alpha": self.target_alpha if is_target else None,
            "region_modes": list(region_modes),
            "clutter_mode": None if is_target else self.clutter_mode,
        }

        self.spawned_objects.append(obj_info)
        self.used_files.add(str(gfile))

        occupied_rects.append(rect)
        if (clutter_rects is not None) and (not is_target):
            clutter_rects.append(rect)

        return obj_info

    def _spawn_target_voxel_surviving(
        self,
        C: ry.Config,
        sim_seconds,
        sim_dt,
        xy_margin,
        z_tolerance,
        max_spawn_attempts=40,
        verbose=True,
    ):
        if self.target_voxel_file is None:
            raise RuntimeError("Target voxel file has not been selected yet.")
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
            print("\n=== Target spawn diagnostics ===")
            print(f"Target voxel file         : {self.target_voxel_file}")
            print(f"Target quarter            : {self.target_quarter_mode}")
            print(f"Target quarter bounds     : x[{qxmin:.4f}, {qxmax:.4f}] y[{qymin:.4f}, {qymax:.4f}]")
            print(f"On-table bounds (margin)  : x[{xmin:.4f}, {xmax:.4f}] y[{ymin:.4f}, {ymax:.4f}]")
            print(f"Table top z               : {table_top:.4f}")
            print(f"z_tolerance               : {z_tolerance:.4f}")
            print(f"Survival threshold z      : {table_top - z_tolerance:.4f}")
            print(f"sim_seconds               : {sim_seconds}")
            print(f"sim_dt                    : {sim_dt}")
            print(f"max_spawn_attempts        : {max_spawn_attempts}")

        for attempt_idx in range(1, max_spawn_attempts + 1):
            if verbose:
                print(f"\n--- Target attempt {attempt_idx}/{max_spawn_attempts} ---")

            target_obj = self._spawn_one_voxel(
                C,
                self.target_voxel_file,
                occupied_rects=[],
                clutter_rects=None,
                region_modes=[self.target_quarter_mode],
                is_target=True,
                force_quarter_center=True,
                ignore_occupancy_for_target=True,
            )

            if target_obj is None:
                if verbose:
                    print("Spawn failed immediately: _spawn_one_voxel returned None.")
                continue

            base_name = f"{target_obj['prefix']}base"

            if base_name not in C.getFrameNames():
                if verbose:
                    print(f"Spawned target base frame missing right after spawn: {base_name}")
                self.remove_objects(C, [target_obj])
                continue

            base_before = C.getFrame(base_name)
            pos_before = np.array(base_before.getPosition(), dtype=float)
            x0, y0, z0 = float(pos_before[0]), float(pos_before[1]), float(pos_before[2])

            if verbose:
                print(f"Spawn prefix              : {target_obj['prefix']}")
                print(f"Spawn basename            : {target_obj['basename']}")
                print(f"Recorded spawn_xy         : {target_obj['spawn_xy']}")
                print(f"Recorded spawn_z          : {target_obj['spawn_z']:.4f}")
                print(f"Recorded theta_deg        : {target_obj['theta_deg']:.2f}")
                print(f"Base pos before sim       : ({x0:.4f}, {y0:.4f}, {z0:.4f})")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            if base_name not in C.getFrameNames():
                if verbose:
                    print("Target disappeared from config after simulation.")
                self.remove_objects(C, [target_obj])
                continue

            base_after = C.getFrame(base_name)
            pos_after = np.array(base_after.getPosition(), dtype=float)
            x1, y1, z1 = float(pos_after[0]), float(pos_after[1]), float(pos_after[2])

            dx = x1 - x0
            dy = y1 - y0
            dz = z1 - z0
            dxy = float(np.sqrt(dx * dx + dy * dy))
            dxyz = float(np.sqrt(dx * dx + dy * dy + dz * dz))

            inside_xy = (xmin <= x1 <= xmax) and (ymin <= y1 <= ymax)
            not_too_low = z1 >= (table_top - z_tolerance)
            survived = inside_xy and not_too_low

            if verbose:
                print(f"Base pos after sim        : ({x1:.4f}, {y1:.4f}, {z1:.4f})")
                print(f"Motion during sim         : dx={dx:.4f}, dy={dy:.4f}, dz={dz:.4f}, dxy={dxy:.4f}, dxyz={dxyz:.4f}")
                print(f"Inside XY bounds?         : {inside_xy}")
                print(f"Above z threshold?        : {not_too_low}")

                if not inside_xy:
                    x_status = xmin <= x1 <= xmax
                    y_status = ymin <= y1 <= ymax
                    print(f"  X valid?                : {x_status}  (allowed [{xmin:.4f}, {xmax:.4f}], got {x1:.4f})")
                    print(f"  Y valid?                : {y_status}  (allowed [{ymin:.4f}, {ymax:.4f}], got {y1:.4f})")

                if not not_too_low:
                    print(f"  Z too low               : threshold {table_top - z_tolerance:.4f}, got {z1:.4f}")

            if survived:
                if verbose:
                    print("Result                    : SUCCESS (target survived on table)")
                return target_obj

            if verbose:
                print("Result                    : FAILED -> removing target and retrying")

            self.remove_objects(C, [target_obj])

        raise RuntimeError(
            "Failed to spawn a target object that survives on the table."
        )

    def spawn_voxels_best_effort(self, C: ry.Config, target_count):
        static_rects = list(self._scene_occupied_rects(C))
        alive_clutter_rects = self._current_alive_object_rects(C, include_target=False)

        occupied_rects = static_rects + alive_clutter_rects
        clutter_rects = list(alive_clutter_rects)

        all_files = self._load_voxel_files()
        usable_files = [f for f in all_files if str(f) not in self.reserved_files]

        unused_files = [f for f in usable_files if str(f) not in self.used_files]
        already_used_files = [f for f in usable_files if str(f) in self.used_files]
        candidate_files = unused_files + already_used_files

        candidate_files = list(candidate_files)
        self.rng.shuffle(candidate_files)

        spawned = []
        attempted = set()

        clutter_regions = (
            self._complement_quarters(self.target_quarter_mode)
            if self.target_quarter_mode is not None
            else self._quarter_modes()
        )

        while len(spawned) < target_count:
            found_one = False

            for gfile in candidate_files:
                gfile_str = str(gfile)
                if gfile_str in attempted:
                    continue

                obj = self._spawn_one_voxel(
                    C,
                    gfile_str,
                    occupied_rects=occupied_rects,
                    clutter_rects=clutter_rects,
                    region_modes=clutter_regions,
                    is_target=False,
                    force_quarter_center=False,
                    ignore_occupancy_for_target=False,
                )
                attempted.add(gfile_str)

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

        del S

    # =========================================================
    # Object validity
    # =========================================================
    def _is_object_on_table(self, C: ry.Config, obj, xy_margin=0.01, z_tolerance=0.15):
        prefix = obj["prefix"]
        base_name = f"{prefix}base"

        if base_name not in C.getFrameNames():
            return False

        base = C.getFrame(base_name)
        pos = np.array(base.getPosition(), dtype=float)
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
    def create_environment_with_refill(
        self,
        num_voxels=15,
        sim_seconds=7.0,
        sim_dt=0.01,
        max_refill_rounds=10,
        xy_margin=0.02,
        z_tolerance=0.15,
        batch_spawn_count=5,
        max_target_spawn_attempts=40,
    ):
        C = self._load_base_scene()
        self._reset_tracking()

        if num_voxels <= 0:
            summary = {
                "target": num_voxels,
                "final_on_table": 0,
                "final_off_table": 0,
                "rounds": 0,
                "batch_spawn_count": batch_spawn_count,
                "clutter_mode": self.clutter_mode,
                "objects": self.spawned_objects,
                "target_voxel_file": None,
                "target_voxel_basename": None,
                "target_original_voxel_basename": None,
                "target_quarter_mode": None,
                "target_object_prefix": None,
                "target_alpha": self.target_alpha,
            }
            return C, summary

        voxel_file = self._choose_target_voxel()
        target_quarter = self._choose_target_quarter()
        self.reserved_files.add(self.target_voxel_file)

        print("Chosen target voxel:", os.path.basename(voxel_file))
        print("Chosen target quarter:", target_quarter)
        print("Clutter mode:", self.clutter_mode)

        clutter_target_count = max(0, num_voxels - 1)
        initial_spawn_count = min(batch_spawn_count, clutter_target_count)

        initially_spawned = self.spawn_voxels_best_effort(C, initial_spawn_count)
        print(f"Initially spawned extra voxels: {len(initially_spawned)} / {initial_spawn_count}")

        round_idx = 0
        while True:
            round_idx += 1
            print(f"\n=== Clutter simulation round {round_idx} ===")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            alive_clutter = [
                obj for obj in self.spawned_objects
                if obj["alive"] and not obj.get("is_target", False)
            ]
            off_clutter = [
                obj for obj in alive_clutter
                if not self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]
            on_clutter = [
                obj for obj in alive_clutter
                if self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]

            print(
                f"Clutter on table: {len(on_clutter)} | "
                f"Off table: {len(off_clutter)} | "
                f"Clutter target: {clutter_target_count}"
            )

            if len(on_clutter) >= clutter_target_count:
                print("Desired number of clutter voxels is on the table.")
                break

            if round_idx >= max_refill_rounds:
                print("Reached max refill rounds for clutter.")
                break

            if off_clutter:
                self.remove_objects(C, off_clutter)

            missing = clutter_target_count - len(on_clutter)
            to_spawn_now = min(batch_spawn_count, missing)

            print(f"Trying to respawn up to {to_spawn_now} clutter voxel(s)...")
            spawned_now = self.spawn_voxels_best_effort(C, to_spawn_now)
            print(f"Respawned {len(spawned_now)} clutter voxel(s).")

            if len(spawned_now) == 0:
                print("Could not spawn any new clutter voxel this round. Stopping clutter refill.")
                break

        alive_clutter = [
            obj for obj in self.spawned_objects
            if obj["alive"] and not obj.get("is_target", False)
        ]
        final_off_clutter = [
            obj for obj in alive_clutter
            if not self._is_object_on_table(
                C,
                obj,
                xy_margin=xy_margin,
                z_tolerance=z_tolerance,
            )
        ]
        if final_off_clutter:
            print(f"Removing {len(final_off_clutter)} final off-table clutter voxel(s).")
            self.remove_objects(C, final_off_clutter)

        print("\n=== Spawning target last ===")
        target_obj = self._spawn_target_voxel_surviving(
            C,
            sim_seconds=sim_seconds,
            sim_dt=sim_dt,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
            max_spawn_attempts=max_target_spawn_attempts,
        )
        print(f"Spawned surviving target voxel: {target_obj['basename']}")

        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        if final_off:
            non_target_final_off = [
                obj for obj in final_off
                if not obj.get("is_target", False)
            ]
            if non_target_final_off:
                print(f"Removing {len(non_target_final_off)} final off-table non-target voxel(s).")
                self.remove_objects(C, non_target_final_off)

        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        alive_target = [obj for obj in final_on if obj.get("is_target", False)]
        if len(alive_target) != 1:
            raise RuntimeError("Final scene does not contain exactly one on-table target object.")

        summary = {
            "target": num_voxels,
            "final_on_table": len(final_on),
            "final_off_table": len(final_off),
            "rounds": round_idx,
            "batch_spawn_count": batch_spawn_count,
            "clutter_mode": self.clutter_mode,
            "objects": self.spawned_objects,
            "target_voxel_file": self.target_voxel_file,
            "target_voxel_basename": (
                f"goal_{os.path.basename(self.target_voxel_file)}"
                if self.target_voxel_file is not None else None
            ),
            "target_original_voxel_basename": (
                os.path.basename(self.target_voxel_file)
                if self.target_voxel_file is not None else None
            ),
            "target_quarter_mode": self.target_quarter_mode,
            "target_object_prefix": self.target_object_prefix,
            "target_alpha": self.target_alpha,
        }

        return C, summary

    # =========================================================
    # Save
    # =========================================================
    def save_environment(self, C: ry.Config, file_name="generated_panda_table_voxel_clutter.g"):
        out_file = self.output_dir / file_name
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(C.write())
        print("Saved:", out_file)
        return str(out_file)