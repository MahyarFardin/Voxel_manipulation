import os
from glob import glob
from pathlib import Path

import numpy as np
import robotic as ry


class PandaTableVoxelClutterGenerator:
    """
    Generates Panda-table voxel scenes with these rules:

    1. One target voxel file is chosen in advance.
    2. One random table quarter is assigned to that target.
    3. Normal clutter voxels are spawned according to clutter_mode:
       - random / low_clutter: in the three non-target quarters
       - high_clutter: in the quarter opposite the target quarter
    4. A normal-opacity copy of the target voxel is also spawned into the clutter
       with the frame prefix 'goal_'.
    5. A translucent copy of the same target voxel is spawned near the center of
       the selected quarter with the frame prefix 'goal_pose_'.
    6. The clutter-side goal_ object has an insertion order controlled by
       hardnessOfTargetObject:
          - 0.0 => as late as possible among clutter drops
          - 1.0 => as early as possible among clutter drops
    7. The final scene is validated so that both:
          - one goal_ object survives on the table
          - one goal_pose_ object survives on the table
    8. The goal_pose_ object uses reduced alpha while preserving RGB.
       The goal_ object keeps its original alpha.

    Non-target clutter placement modes:
    - "random": purely random inside the 3 non-target quarters, no clutter overlap check
    - "low_clutter": best-effort spread-out placement in the 3 non-target quarters
    - "high_clutter": prefers placement close to existing clutter, creating dense clusters,
      and samples clutter only from the quarter opposite the target quarter
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
        hardnessOfTargetObject=0.0,
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

        self.hardnessOfTargetObject = float(hardnessOfTargetObject)
        if not (0.0 <= self.hardnessOfTargetObject <= 1.0):
            raise ValueError("hardnessOfTargetObject must be between 0 and 1.")

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

        self.goal_clutter_object_prefix = None
        self.goal_pose_object_prefix = None

        self.goal_clutter_insert_index = None
        self.clutter_spawn_success_count = 0
        self.goal_clutter_has_spawned_once = False

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
        """
        Returns the quarter(s) used for spawning non-goal_pose clutter.

        Rules:
        - if no target quarter is known yet, allow all quarters
        - for random / low_clutter: allow the 3 non-target quarters
        - for high_clutter: allow only the quarter opposite the target quarter
        """
        if self.target_quarter_mode is None:
            return self._quarter_modes()

        if self.clutter_mode == "high_clutter":
            return [self._opposite_quarter(self.target_quarter_mode)]

        return self._complement_quarters(self.target_quarter_mode)

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
            if nm.startswith("obj") or nm.startswith("goal_") or nm.startswith("goal_pose_"):
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

            if (not include_target) and (not obj.get("counts_as_clutter", False)):
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

    def _alive_on_table_objects(self, C: ry.Config, xy_margin=0.02, z_tolerance=0.15):
        alive = [obj for obj in self.spawned_objects if obj["alive"]]
        on_table = [
            obj for obj in alive
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
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0

        self.target_voxel_file = None
        self.target_quarter_mode = None

        self.goal_clutter_object_prefix = None
        self.goal_pose_object_prefix = None

        self.goal_clutter_insert_index = None
        self.clutter_spawn_success_count = 0
        self.goal_clutter_has_spawned_once = False

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


    def _disable_goal_pose_contact(self, C: ry.Config):
        """
        Disables contact for all frames belonging to the surviving goal_pose object.
        This is intended to be called at the very end, right before saving.
        """
        if self.goal_pose_object_prefix is None:
            return

        prefix = self.goal_pose_object_prefix
        matching_names = [nm for nm in C.getFrameNames() if nm.startswith(prefix)]

        for nm in matching_names:
            fr = C.getFrame(nm)
            if "cube" in nm:
                if fr is None:
                    continue
                try:
                    fr.setContact(0)
                except Exception:
                    pass

    def _compute_goal_clutter_insert_index(self, clutter_total_count: int):
        """
        clutter_total_count includes:
          - normal clutter voxels
          - exactly one goal_... clutter target voxel

        hardnessOfTargetObject:
          1.0 -> inserted first among clutter drops
          0.0 -> inserted last among clutter drops
        """
        if clutter_total_count <= 0:
            return None
        return int(round((1.0 - self.hardnessOfTargetObject) * (clutter_total_count - 1)))

    def _has_alive_role(self, role: str):
        return any(
            obj["alive"] and obj.get("role") == role
            for obj in self.spawned_objects
        )

    def _should_spawn_goal_clutter_now(self):
        """
        The goal_... clutter object is spawned exactly once as part of clutter creation.
        Before its first spawn, its position in the drop order is controlled by
        hardnessOfTargetObject. After it has existed once, if it falls off and needs
        respawn, it becomes eligible immediately.
        """
        if self.target_voxel_file is None:
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
        object_role="normal",   # "normal", "goal", "goal_pose"
        force_quarter_center=False,
        ignore_occupancy_for_target=False,
    ):
        cubes = self._voxel_cube_geometry(gfile)
        local_min, _ = self._local_aabb(cubes)

        theta = float(self.rng.uniform(0.0, 2.0 * np.pi))
        _, _, rot_size_xy = self._rotated_xy_aabb_size(cubes, theta)

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
        z = float(table_info["top_z"] - local_min[2] + self.spawn_height)

        prefix_core = f"{self.object_counter}_"
        if object_role == "normal":
            prefix = f"obj{prefix_core}"
        elif object_role == "goal":
            prefix = f"goal_{prefix_core}"
        elif object_role == "goal_pose":
            prefix = f"goal_pose_{prefix_core}"
        else:
            raise ValueError(f"Unknown object_role: {object_role}")

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

        if object_role == "goal_pose":
            self._set_target_alpha(C, prefix, self.target_alpha)

        basename = os.path.basename(gfile)
        if object_role == "normal":
            reported_basename = basename
        elif object_role == "goal":
            reported_basename = f"goal_{basename}"
        else:
            reported_basename = f"goal_pose_{basename}"

        counts_as_clutter = object_role in {"normal", "goal"}

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
            "role": object_role,
            "counts_as_clutter": counts_as_clutter,
            "is_target_family": object_role in {"goal", "goal_pose"},
            "target_alpha": self.target_alpha if object_role == "goal_pose" else None,
            "region_modes": list(region_modes),
            "clutter_mode": self.clutter_mode if counts_as_clutter else None,
        }

        self.spawned_objects.append(obj_info)
        self.used_files.add(str(gfile))

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
        """
        Ensures there is exactly one surviving on-table goal_... clutter object.
        If goal_ is missing or fell off, this keeps respawning it in the clutter
        until one survives.
        """
        if self.target_voxel_file is None:
            raise RuntimeError("Target voxel file has not been selected yet.")
        if self.target_quarter_mode is None:
            raise RuntimeError("Target quarter has not been selected yet.")

        clutter_regions = self._clutter_region_modes()
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=xy_margin)
        table_top = self._get_table_info(C)["top_z"]

        if verbose:
            print("\n=== Final goal_ clutter survival check ===")
            print(f"Target voxel file         : {self.target_voxel_file}")
            print(f"Target quarter            : {self.target_quarter_mode}")
            print(f"Allowed clutter regions   : {clutter_regions}")
            print(f"On-table bounds (margin)  : x[{xmin:.4f}, {xmax:.4f}] y[{ymin:.4f}, {ymax:.4f}]")
            print(f"Table top z               : {table_top:.4f}")
            print(f"z_tolerance               : {z_tolerance:.4f}")
            print(f"Survival threshold z      : {table_top - z_tolerance:.4f}")
            print(f"max_spawn_attempts        : {max_spawn_attempts}")

        for attempt_idx in range(1, max_spawn_attempts + 1):
            if verbose:
                print(f"\n--- goal_ attempt {attempt_idx}/{max_spawn_attempts} ---")

            alive_goals = [
                obj for obj in self.spawned_objects
                if obj["alive"] and obj.get("role") == "goal"
            ]
            alive_goal_on_table = [
                obj for obj in alive_goals
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

            goal_obj = self._spawn_one_voxel(
                C,
                self.target_voxel_file,
                occupied_rects=occupied_rects,
                clutter_rects=clutter_rects,
                region_modes=clutter_regions,
                object_role="goal",
                force_quarter_center=False,
                ignore_occupancy_for_target=False,
            )

            if goal_obj is None:
                if verbose:
                    print("Spawn failed immediately: _spawn_one_voxel returned None.")
                continue

            base_name = f"{goal_obj['prefix']}base"
            if base_name not in C.getFrameNames():
                if verbose:
                    print(f"Spawned goal_ base frame missing right after spawn: {base_name}")
                self.remove_objects(C, [goal_obj])
                continue

            base_before = C.getFrame(base_name)
            pos_before = np.array(base_before.getPosition(), dtype=float)
            x0, y0, z0 = float(pos_before[0]), float(pos_before[1]), float(pos_before[2])

            if verbose:
                print(f"Spawn prefix              : {goal_obj['prefix']}")
                print(f"Spawn basename            : {goal_obj['basename']}")
                print(f"Recorded spawn_xy         : {goal_obj['spawn_xy']}")
                print(f"Recorded spawn_z          : {goal_obj['spawn_z']:.4f}")
                print(f"Recorded theta_deg        : {goal_obj['theta_deg']:.2f}")
                print(f"Base pos before sim       : ({x0:.4f}, {y0:.4f}, {z0:.4f})")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            if base_name not in C.getFrameNames():
                if verbose:
                    print("goal_ disappeared from config after simulation.")
                self.remove_objects(C, [goal_obj])
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

            if survived:
                if verbose:
                    print("Result                    : SUCCESS (goal_ survived on table)")
                return goal_obj

            if verbose:
                print("Result                    : FAILED -> removing goal_ and retrying")

            self.remove_objects(C, [goal_obj])

        raise RuntimeError(
            "Failed to obtain a surviving on-table goal_ clutter object."
        )

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
        """
        Spawns the translucent goal_pose_... object in the selected quarter, after the
        clutter has already been generated and after goal_ has been validated.
        """
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
            print("\n=== goal_pose spawn diagnostics ===")
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
                print(f"\n--- goal_pose attempt {attempt_idx}/{max_spawn_attempts} ---")

            target_obj = self._spawn_one_voxel(
                C,
                self.target_voxel_file,
                occupied_rects=[],
                clutter_rects=None,
                region_modes=[self.target_quarter_mode],
                object_role="goal_pose",
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
                    print(f"Spawned goal_pose base frame missing right after spawn: {base_name}")
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
                    print("goal_pose disappeared from config after simulation.")
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

            if survived:
                if verbose:
                    print("Result                    : SUCCESS (goal_pose survived on table)")
                return target_obj

            if verbose:
                print("Result                    : FAILED -> removing goal_pose and retrying")

            self.remove_objects(C, [target_obj])

        raise RuntimeError(
            "Failed to spawn a goal_pose object that survives on the table."
        )

    def spawn_voxels_best_effort(self, C: ry.Config, target_count):
        """
        target_count counts all clutter objects to be spawned in this call, including
        the special goal_... clutter target object if it becomes eligible here.
        """
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
        attempted_normal_files = set()

        clutter_regions = self._clutter_region_modes()

        while len(spawned) < target_count:
            found_one = False

            if self._should_spawn_goal_clutter_now():
                goal_obj = self._spawn_one_voxel(
                    C,
                    self.target_voxel_file,
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
                else:
                    break

            for gfile in candidate_files:
                gfile_str = str(gfile)
                if gfile_str in attempted_normal_files:
                    continue

                obj = self._spawn_one_voxel(
                    C,
                    gfile_str,
                    occupied_rects=occupied_rects,
                    clutter_rects=clutter_rects,
                    region_modes=clutter_regions,
                    object_role="normal",
                    force_quarter_center=False,
                    ignore_occupancy_for_target=False,
                )
                attempted_normal_files.add(gfile_str)

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
        """
        New semantics:
          - num_voxels = number of clutter objects desired on the table
          - that count INCLUDES exactly one goal_... object
          - after clutter is done, one extra goal_pose_... object is spawned
          - final total object count is at least num_voxels + 1
        """
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
                "target_original_voxel_basename": None,
                "target_quarter_mode": None,
                "goal_clutter_object_prefix": None,
                "goal_pose_object_prefix": None,
                "target_alpha": self.target_alpha,
                "hardnessOfTargetObject": self.hardnessOfTargetObject,
                "goal_clutter_insert_index": None,
            }
            return C, summary

        voxel_file = self._choose_target_voxel()
        target_quarter = self._choose_target_quarter()
        self.reserved_files.add(self.target_voxel_file)

        clutter_target_count = int(num_voxels)
        self.goal_clutter_insert_index = self._compute_goal_clutter_insert_index(clutter_target_count)

        print("Chosen target voxel:", os.path.basename(voxel_file))
        print("Chosen target quarter:", target_quarter)
        print("Clutter mode:", self.clutter_mode)
        print("hardnessOfTargetObject:", self.hardnessOfTargetObject)
        print("goal_ clutter insert index:", self.goal_clutter_insert_index)

        if self.clutter_mode == "high_clutter":
            print("Opposite clutter quarter:", self._opposite_quarter(target_quarter))

        initial_spawn_count = min(batch_spawn_count, clutter_target_count)
        initially_spawned = self.spawn_voxels_best_effort(C, initial_spawn_count)
        print(f"Initially spawned clutter voxels: {len(initially_spawned)} / {initial_spawn_count}")

        round_idx = 0
        while True:
            round_idx += 1
            print(f"\n=== Clutter simulation round {round_idx} ===")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            alive_clutter = [
                obj for obj in self.spawned_objects
                if obj["alive"] and obj.get("counts_as_clutter", False)
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
                obj for obj in self.spawned_objects
                if obj["alive"] and obj.get("counts_as_clutter", False)
            ]
            on_clutter_after_removal = [
                obj for obj in alive_clutter_after_removal
                if self._is_object_on_table(
                    C,
                    obj,
                    xy_margin=xy_margin,
                    z_tolerance=z_tolerance,
                )
            ]
            goal_on_after_removal = [
                obj for obj in on_clutter_after_removal
                if obj.get("role") == "goal"
            ]

            dynamic_clutter_target_after_removal = clutter_target_count + (
                0 if len(goal_on_after_removal) == 1 else 1
            )

            missing = dynamic_clutter_target_after_removal - len(on_clutter_after_removal)
            to_spawn_now = min(batch_spawn_count, max(0, missing))

            print(
                f"Trying to respawn up to {to_spawn_now} clutter voxel(s)... "
                f"(goal present on table? {'yes' if len(goal_on_after_removal) == 1 else 'no'})"
            )

            spawned_now = self.spawn_voxels_best_effort(C, to_spawn_now)
            print(f"Respawned {len(spawned_now)} clutter voxel(s).")

            if len(spawned_now) == 0:
                print("Could not spawn any new clutter voxel this round. Stopping clutter refill.")
                break

        alive_clutter = [
            obj for obj in self.spawned_objects
            if obj["alive"] and obj.get("counts_as_clutter", False)
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

        print("\n=== Final rescue check for goal_ ===")
        goal_obj = self._spawn_goal_clutter_surviving(
            C,
            sim_seconds=sim_seconds,
            sim_dt=sim_dt,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
            max_spawn_attempts=max_target_spawn_attempts,
        )
        print(f"Confirmed surviving goal_ voxel: {goal_obj['basename']}")

        print("\n=== Spawning goal_pose last ===")
        goal_pose_obj = self._spawn_target_voxel_surviving(
            C,
            sim_seconds=sim_seconds,
            sim_dt=sim_dt,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
            max_spawn_attempts=max_target_spawn_attempts,
        )
        print(f"Spawned surviving goal_pose voxel: {goal_pose_obj['basename']}")

        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        if final_off:
            final_off_non_pose = [
                obj for obj in final_off
                if obj.get("role") != "goal_pose"
            ]
            if final_off_non_pose:
                print(f"Removing {len(final_off_non_pose)} final off-table non-goal_pose voxel(s).")
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

        summary = {
            "target": num_voxels,
            "final_on_table": len(final_on),
            "final_off_table": len(final_off),
            "rounds": round_idx,
            "batch_spawn_count": batch_spawn_count,
            "clutter_mode": self.clutter_mode,
            "objects": self.spawned_objects,
            "target_voxel_file": self.target_voxel_file,
            "target_original_voxel_basename": (
                os.path.basename(self.target_voxel_file)
                if self.target_voxel_file is not None else None
            ),
            "goal_clutter_voxel_basename": (
                f"goal_{os.path.basename(self.target_voxel_file)}"
                if self.target_voxel_file is not None else None
            ),
            "goal_pose_voxel_basename": (
                f"goal_pose_{os.path.basename(self.target_voxel_file)}"
                if self.target_voxel_file is not None else None
            ),
            "target_quarter_mode": self.target_quarter_mode,
            "goal_clutter_object_prefix": self.goal_clutter_object_prefix,
            "goal_pose_object_prefix": self.goal_pose_object_prefix,
            "target_alpha": self.target_alpha,
            "hardnessOfTargetObject": self.hardnessOfTargetObject,
            "goal_clutter_insert_index": self.goal_clutter_insert_index,
        }

        return C, summary

    # =========================================================
    # Save
    # =========================================================
    def save_environment(self, C: ry.Config, file_name="generated_panda_table_voxel_clutter.g"):
        self._disable_goal_pose_contact(C)

        out_file = self.output_dir / file_name
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(C.write())
        print("Saved:", out_file)
        return str(out_file)