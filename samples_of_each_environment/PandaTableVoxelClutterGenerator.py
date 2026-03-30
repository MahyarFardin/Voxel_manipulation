import os
from glob import glob
from pathlib import Path

import numpy as np
import robotic as ry


class PandaTableVoxelClutterGenerator:
    """
    PandaTableVoxelClutterGenerator
    ===============================

    This class generates cluttered Panda-table scenes containing:
    1. A Panda robot and table loaded from a base RAI scene.
    2. Multiple voxel objects loaded from pre-generated voxel .g files.
    3. Optionally, a thin 2D marker ("shadow"/target surface) placed on the
       opposite half of the table, representing one stable resting face of a
       chosen target voxel.

    Main pipeline
    -------------
    1. Load base scene.
    2. Optionally choose a target voxel and one stable resting face.
    3. Place a 2D marker of that face on the opposite half of the table.
    4. Spawn the matching target voxel into the clutter half.
    5. Spawn extra clutter voxels above the table.
    6. Simulate physics so objects settle.
    7. Remove objects that fell off / are invalid.
    8. Refill missing ones and repeat.
    9. Before returning, remove any final remaining off-table voxels so the
       returned config matches what "final_on_table" says.

    Important fixes in this version
    -------------------------------
    - Final off-table objects are removed before returning.
      So you should no longer see extra voxels on the ground in the final config.
    - The target voxel file name and the target 2D marker parent frame name are
      returned in the summary.
    - The 2D target marker is now created under a single parent frame:
          targetSurface
      and its colored tiles are children of that frame.

    Split-table generation
    ----------------------
    Supported spawn_half_mode values:
    - None
    - "front" : lower-y half
    - "back"  : upper-y half
    - "left"  : lower-x half
    - "right" : upper-x half

    Voxels spawn in the chosen half, while the target marker is placed in the
    opposite half.

    Parameters
    ----------
    base_scene_file : str or Path
        Path to the base Panda/table scene.

    voxel_dir : str or Path
        Folder containing voxel .g files.

    output_dir : str or Path
        Folder where generated environments can be saved.

    table_frame_name : str
        Name of the table frame in the scene.

    gap : float
        Extra spacing margin used during XY placement.

    spawn_height : float
        Height above the table from which objects are dropped.

    seed : int
        Random seed.

    per_cube_mass : float
        Mass assigned to each cube of a voxel object.

    table_shape_size : tuple
        Replacement table size: (x_size, y_size, z_size, rounding).

    panda_base_relative_pos : tuple
        Relative position for frame 'l_panda_base'.

    marker_thickness : float
        Thickness of the 2D target marker tiles.

    spawn_half_mode : None or str
        Restrict spawning to one half of the table.
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
        marker_thickness=0.004,
        spawn_half_mode=None,
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
        self.marker_thickness = float(marker_thickness)

        valid_modes = {None, "front", "back", "left", "right"}
        if spawn_half_mode not in valid_modes:
            raise ValueError(
                f"spawn_half_mode must be one of {valid_modes}, got: {spawn_half_mode}"
            )
        self.spawn_half_mode = spawn_half_mode

        if not self.base_scene_file.exists():
            raise FileNotFoundError(f"Base scene file not found: {self.base_scene_file}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.rng = np.random.default_rng(self.seed)

        # Tracking for current environment generation
        self.spawned_objects = []
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0
        self.static_rects = []

        self.target_surface_info = None
        self.target_voxel_file = None
        self.target_surface_choice = None

    # =========================================================
    # Basic helpers
    # =========================================================
    def _cube_frames(self, C: ry.Config, prefix: str):
        """Return all cube frame names starting with the given prefix."""
        return [n for n in C.getFrameNames() if n.startswith(prefix) and "cube" in n]

    def _quat_from_z_rotation(self, theta: float):
        """Quaternion [w, x, y, z] for pure z-axis rotation."""
        return [float(np.cos(theta / 2.0)), 0.0, 0.0, float(np.sin(theta / 2.0))]

    def _load_voxel_files(self):
        """Load all voxel .g files from the voxel directory."""
        voxel_files = sorted(glob(str(self.voxel_dir / "*.g")))
        if not voxel_files:
            raise FileNotFoundError(f"No voxel files found in: {self.voxel_dir}")
        return voxel_files

    def _load_base_scene(self):
        """
        Load the Panda/table base scene and apply:
        - table geometry override
        - Panda base relative position override
        """
        C = ry.Config()
        C.addFile(str(self.base_scene_file))

        if self.table_frame_name not in C.getFrameNames():
            raise ValueError(f"Table frame '{self.table_frame_name}' not found in scene.")

        if "l_panda_base" not in C.getFrameNames():
            raise ValueError("Frame 'l_panda_base' not found in scene.")

        C.getFrame(self.table_frame_name).setShape(
            ry.ST.ssBox,
            self.table_shape_size
        )

        C.getFrame("l_panda_base").setRelativePosition(
            self.panda_base_relative_pos
        )

        return C

    # =========================================================
    # Scene geometry
    # =========================================================
    def _get_table_info(self, C: ry.Config):
        """Return table frame, center, size, and top z."""
        if self.table_frame_name not in C.getFrameNames():
            raise ValueError(f"Table frame '{self.table_frame_name}' not found in scene.")

        table = C.getFrame(self.table_frame_name)
        table_pos = np.array(table.getPosition(), dtype=float)
        table_size = np.array(table.getSize(), dtype=float)

        if len(table_size) < 3:
            raise ValueError(
                f"Table frame '{self.table_frame_name}' does not have a valid box size."
            )

        tx, ty, tz = float(table_size[0]), float(table_size[1]), float(table_size[2])
        px, py, pz = float(table_pos[0]), float(table_pos[1]), float(table_pos[2])

        return {
            "frame": table,
            "pos": np.array([px, py, pz], dtype=float),
            "size": np.array([tx, ty, tz], dtype=float),
            "top_z": pz + tz / 2.0,
        }

    def _table_bounds_xy(self, C: ry.Config, margin=0.0):
        """Return full table XY bounds as (xmin, xmax, ymin, ymax)."""
        info = self._get_table_info(C)
        tx, ty, _ = info["size"]
        px, py, _ = info["pos"]

        xmin = px - tx / 2.0 + margin
        xmax = px + tx / 2.0 - margin
        ymin = py - ty / 2.0 + margin
        ymax = py + ty / 2.0 - margin
        return xmin, xmax, ymin, ymax

    def _opposite_half_mode(self, half_mode):
        """Return opposite split-table mode."""
        if half_mode is None:
            return None
        if half_mode == "front":
            return "back"
        if half_mode == "back":
            return "front"
        if half_mode == "left":
            return "right"
        if half_mode == "right":
            return "left"
        raise ValueError(f"Unknown half mode: {half_mode}")

    def _spawn_region_bounds_xy(self, C: ry.Config, margin=0.0, half_mode=None):
        """
        Return XY bounds of the active placement region.
        If half_mode is None, self.spawn_half_mode is used.
        """
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=margin)

        if half_mode is None:
            half_mode = self.spawn_half_mode

        if half_mode is None:
            return xmin, xmax, ymin, ymax

        xmid = 0.5 * (xmin + xmax)
        ymid = 0.5 * (ymin + ymax)

        if half_mode == "front":
            return xmin, xmax, ymin, ymid
        if half_mode == "back":
            return xmin, xmax, ymid, ymax
        if half_mode == "left":
            return xmin, xmid, ymin, ymax
        if half_mode == "right":
            return xmid, xmax, ymin, ymax

        raise ValueError(f"Unknown half mode: {half_mode}")

    def _voxel_cube_geometry(self, file_path: str):
        """
        Load a voxel file temporarily and extract per-cube local geometry:
        - name
        - local position
        - size
        - color
        """
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
        """Compute local 3D AABB of a voxel from its cubes."""
        min_corner = np.array([np.inf, np.inf, np.inf], dtype=float)
        max_corner = np.array([-np.inf, -np.inf, -np.inf], dtype=float)

        for cube in cubes:
            pos = cube["pos"]
            half = cube["size"] / 2.0
            min_corner = np.minimum(min_corner, pos - half)
            max_corner = np.maximum(max_corner, pos + half)

        return min_corner, max_corner

    def _rotated_xy_aabb_size(self, cubes, theta: float):
        """
        Compute the rotated XY AABB of a voxel after z rotation by theta.
        Returns (min_xy, max_xy, size_xy).
        """
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
        """Check overlap of two axis-aligned XY rectangles."""
        x1_min, x1_max, y1_min, y1_max = rect1
        x2_min, x2_max, y2_min, y2_max = rect2

        return not (
            x1_max + extra_gap <= x2_min or
            x2_max + extra_gap <= x1_min or
            y1_max + extra_gap <= y2_min or
            y2_max + extra_gap <= y1_min
        )

    # =========================================================
    # 2D stability helpers
    # =========================================================
    def _cross2d(self, o, a, b):
        """Signed 2D cross product used in convex hull tests."""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _convex_hull_2d(self, points):
        """Monotonic-chain convex hull."""
        pts = sorted(set((float(p[0]), float(p[1])) for p in points))
        if len(pts) <= 1:
            return pts

        lower = []
        for p in pts:
            while len(lower) >= 2 and self._cross2d(lower[-2], lower[-1], p) <= 1e-12:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and self._cross2d(upper[-2], upper[-1], p) <= 1e-12:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

    def _point_on_segment_2d(self, p, a, b, tol=1e-9):
        """Check if p lies on segment a-b."""
        ap = np.array(p) - np.array(a)
        ab = np.array(b) - np.array(a)
        cross = abs(ab[0] * ap[1] - ab[1] * ap[0])
        if cross > tol:
            return False
        dot = np.dot(ap, ab)
        if dot < -tol:
            return False
        if dot > np.dot(ab, ab) + tol:
            return False
        return True

    def _point_in_convex_polygon_2d(self, p, poly, tol=1e-9):
        """Check if point p is inside or on a convex polygon."""
        if len(poly) == 0:
            return False
        if len(poly) == 1:
            return np.linalg.norm(np.array(p) - np.array(poly[0])) <= tol
        if len(poly) == 2:
            return self._point_on_segment_2d(p, poly[0], poly[1], tol=tol)

        sign = None
        for i in range(len(poly)):
            a = np.array(poly[i], dtype=float)
            b = np.array(poly[(i + 1) % len(poly)], dtype=float)
            c = self._cross2d(a, b, p)

            if abs(c) <= tol:
                continue

            current = c > 0
            if sign is None:
                sign = current
            elif sign != current:
                return False

        return True

    # =========================================================
    # Stable resting-surface analysis
    # =========================================================
    def _cube_com(self, cubes):
        """Approximate center of mass by volume-weighted cube centers."""
        masses = []
        centers = []

        for cube in cubes:
            size = cube["size"]
            volume = float(size[0] * size[1] * size[2])
            masses.append(volume)
            centers.append(cube["pos"])

        masses = np.array(masses, dtype=float)
        centers = np.array(centers, dtype=float)

        total_mass = masses.sum()
        if total_mass <= 0:
            return centers.mean(axis=0)

        return (centers * masses[:, None]).sum(axis=0) / total_mass

    def _resting_surface_info(self, cubes, axis, use_max_side, tol=1e-8):
        """
        Analyze one candidate support face and determine if it is stable.
        A face is stable if the COM projection lies inside the support hull.
        """
        other_axes = [ax for ax in [0, 1, 2] if ax != axis]

        if use_max_side:
            plane_val = max(c["pos"][axis] + c["size"][axis] / 2.0 for c in cubes)
            touching = [
                c for c in cubes
                if abs((c["pos"][axis] + c["size"][axis] / 2.0) - plane_val) <= tol
            ]
            side_name = f"+{'xyz'[axis]}"
        else:
            plane_val = min(c["pos"][axis] - c["size"][axis] / 2.0 for c in cubes)
            touching = [
                c for c in cubes
                if abs((c["pos"][axis] - c["size"][axis] / 2.0) - plane_val) <= tol
            ]
            side_name = f"-{'xyz'[axis]}"

        if len(touching) == 0:
            return None

        support_rects = []
        corners = []
        min_xy = np.array([np.inf, np.inf], dtype=float)
        max_xy = np.array([-np.inf, -np.inf], dtype=float)

        for cube in touching:
            center_2d = cube["pos"][other_axes]
            size_2d = cube["size"][other_axes]
            half_2d = size_2d / 2.0

            lo = center_2d - half_2d
            hi = center_2d + half_2d

            support_rects.append({
                "center_2d": center_2d.copy(),
                "size_2d": size_2d.copy(),
                "lo": lo.copy(),
                "hi": hi.copy(),
                "color": list(cube["color"]),
                "source_cube_name": cube["name"],
            })

            min_xy = np.minimum(min_xy, lo)
            max_xy = np.maximum(max_xy, hi)

            corners.extend([
                (lo[0], lo[1]),
                (lo[0], hi[1]),
                (hi[0], lo[1]),
                (hi[0], hi[1]),
            ])

        hull = self._convex_hull_2d(corners)
        com = self._cube_com(cubes)
        com_proj = com[other_axes]
        stable = self._point_in_convex_polygon_2d(com_proj, hull, tol=1e-8)

        return {
            "axis": axis,
            "use_max_side": use_max_side,
            "side_name": side_name,
            "other_axes": other_axes,
            "plane_val": float(plane_val),
            "touching_cubes": touching,
            "support_rects": support_rects,
            "support_hull": hull,
            "com": com,
            "com_proj": com_proj,
            "stable": bool(stable),
            "bbox_min_2d": min_xy,
            "bbox_max_2d": max_xy,
            "bbox_size_2d": max_xy - min_xy,
        }

    def _stable_resting_surfaces(self, cubes):
        """Return all stable axis-aligned outer support faces."""
        surfaces = []
        for axis in [0, 1, 2]:
            for use_max_side in [False, True]:
                info = self._resting_surface_info(cubes, axis, use_max_side)
                if info is not None and info["stable"]:
                    surfaces.append(info)
        return surfaces

    # =========================================================
    # Occupancy helpers
    # =========================================================
    def _frame_xy_rect(self, fr):
        """
        Approximate a frame by an XY rectangle using its size and position.
        Returns None if no meaningful size exists.
        """
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
        """
        Collect XY rectangles already occupying table space.

        Excluded:
        - spawned voxel frames (obj*)
        - the table itself
        - target surface parent and tiles
        """
        rects = []
        names = C.getFrameNames()

        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=0.0)

        for nm in names:
            if nm.startswith("obj"):
                continue
            if nm == self.table_frame_name:
                continue
            if nm == "targetSurface" or nm.startswith("targetSurface_"):
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

        rects.extend(self.static_rects)
        return rects

    # =========================================================
    # Tracking reset
    # =========================================================
    def _reset_tracking(self):
        """Reset per-environment state."""
        self.spawned_objects = []
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0
        self.static_rects = []
        self.target_surface_info = None
        self.target_voxel_file = None
        self.target_surface_choice = None

    # =========================================================
    # Target voxel selection
    # =========================================================
    def _choose_target_voxel_and_side(self):
        """
        Choose:
        1. one voxel uniformly among eligible voxel files,
        2. one stable side uniformly from that voxel.
        """
        voxel_files = self._load_voxel_files()
        eligible = []

        for vf in voxel_files:
            cubes = self._voxel_cube_geometry(str(vf))
            stable_surfaces = self._stable_resting_surfaces(cubes)
            if len(stable_surfaces) > 0:
                eligible.append((str(vf), cubes, stable_surfaces))

        if len(eligible) == 0:
            raise RuntimeError("Could not find any voxel with at least one stable resting side.")

        chosen_idx = int(self.rng.integers(len(eligible)))
        voxel_file, cubes, stable_surfaces = eligible[chosen_idx]

        side_idx = int(self.rng.integers(len(stable_surfaces)))
        surface = stable_surfaces[side_idx]

        self.target_voxel_file = voxel_file
        self.target_surface_choice = surface

        return voxel_file, cubes, surface

    def _place_target_surface_marker(self, C: ry.Config):
        """
        Place a 2D colored marker for the chosen target face.

        Implementation detail:
        - A single parent frame 'targetSurface' is created.
        - Each colored tile becomes a child frame under it.
        - This gives one marker parent frame name that can be returned.
        """
        if self.target_voxel_file is None or self.target_surface_choice is None:
            raise RuntimeError("Target voxel/side has not been chosen yet.")

        voxel_file = self.target_voxel_file
        surface = self.target_surface_choice

        size_xy = surface["bbox_size_2d"]
        marker_half_mode = self._opposite_half_mode(self.spawn_half_mode)

        placed_rects = self._scene_occupied_rects(C)
        cx, cy, rect = self._sample_noncolliding_xy(
            C,
            size_xy,
            placed_rects,
            half_mode=marker_half_mode,
        )

        table_info = self._get_table_info(C)
        z_marker = table_info["top_z"] + self.marker_thickness / 2.0

        local_center_2d = 0.5 * (surface["bbox_min_2d"] + surface["bbox_max_2d"])

        marker_parent_name = "targetSurface"
        tile_names = []

        # Remove stale targetSurface if somehow present
        if marker_parent_name in C.getFrameNames():
            C.delFrame(marker_parent_name)

        C.addFrame(marker_parent_name).setPosition([cx, cy, z_marker])

        for i, r in enumerate(surface["support_rects"]):
            tile_center_local = r["center_2d"] - local_center_2d

            sx = float(r["size_2d"][0])
            sy = float(r["size_2d"][1])
            tile_color = [float(c) for c in r["color"][:3]]

            nm = f"{marker_parent_name}_tile_{i}"
            C.addFrame(nm, marker_parent_name) \
                .setShape(ry.ST.ssBox, size=[sx, sy, self.marker_thickness, 0.001]) \
                .setColor(tile_color) \
                .setRelativePosition([
                    float(tile_center_local[0]),
                    float(tile_center_local[1]),
                    0.0,
                ])

            tile_names.append(nm)

        self.static_rects.append(rect)

        self.target_surface_info = {
            "voxel_file": voxel_file,
            "voxel_basename": os.path.basename(voxel_file),
            "side_name": surface["side_name"],
            "axis": surface["axis"],
            "use_max_side": surface["use_max_side"],
            "stable": surface["stable"],
            "support_cube_count": len(surface["touching_cubes"]),
            "marker_center_xy": (cx, cy),
            "marker_rect": rect,
            "marker_frame_name": marker_parent_name,
            "marker_tile_names": tile_names,
            "support_bbox_size_2d": surface["bbox_size_2d"].tolist(),
            "com_local": surface["com"].tolist(),
            "com_proj_local": surface["com_proj"].tolist(),
            "spawn_half_mode": self.spawn_half_mode,
            "marker_half_mode": marker_half_mode,
        }

        return self.target_surface_info

    def spawn_target_voxel(self, C: ry.Config):
        """Spawn the chosen target voxel into the scene."""
        if self.target_voxel_file is None:
            raise RuntimeError("Target voxel file has not been selected yet.")

        placed_rects = self._scene_occupied_rects(C)
        obj = self._spawn_one_voxel(C, self.target_voxel_file, placed_rects)
        return obj

    # =========================================================
    # Placement / spawning
    # =========================================================
    def _sample_noncolliding_xy(
        self,
        C: ry.Config,
        size_xy,
        placed_rects,
        max_tries=3000,
        half_mode=None,
    ):
        """
        Sample a random XY position for a rectangle of size size_xy such that:
        - it lies inside the allowed region,
        - it does not overlap already occupied rectangles.
        """
        xmin, xmax, ymin, ymax = self._spawn_region_bounds_xy(
            C,
            margin=0.0,
            half_mode=half_mode,
        )

        half_x = size_xy[0] / 2.0
        half_y = size_xy[1] / 2.0

        x_min = xmin + half_x + self.gap
        x_max = xmax - half_x - self.gap
        y_min = ymin + half_y + self.gap
        y_max = ymax - half_y - self.gap

        resolved_half_mode = half_mode if half_mode is not None else self.spawn_half_mode

        if x_min > x_max or y_min > y_max:
            raise ValueError(
                f"Allowed region too small for an object of size {size_xy} "
                f"under mode '{resolved_half_mode}'."
            )

        for _ in range(max_tries):
            x = float(self.rng.uniform(x_min, x_max))
            y = float(self.rng.uniform(y_min, y_max))
            rect = (x - half_x, x + half_x, y - half_y, y + half_y)

            collides = any(
                self._rectangles_overlap(rect, other, extra_gap=self.gap)
                for other in placed_rects
            )
            if not collides:
                return x, y, rect

        raise RuntimeError(
            "Could not find non-colliding position "
            f"in half_mode={resolved_half_mode}."
        )

    def _spawn_one_voxel(self, C: ry.Config, gfile: str, placed_rects):
        """
        Spawn one voxel object:
        - compute random rotation
        - estimate rotated footprint
        - sample collision-free XY
        - place above table
        - enable contact and mass
        """
        cubes = self._voxel_cube_geometry(gfile)
        local_min, _ = self._local_aabb(cubes)

        theta = float(self.rng.uniform(0.0, 2.0 * np.pi))
        _, _, rot_size_xy = self._rotated_xy_aabb_size(cubes, theta)

        try:
            x, y, rect = self._sample_noncolliding_xy(
                C,
                rot_size_xy,
                placed_rects,
                half_mode=self.spawn_half_mode,
            )
        except RuntimeError:
            return None

        table_info = self._get_table_info(C)
        z = float(table_info["top_z"] - local_min[2] + self.spawn_height)

        prefix = f"obj{self.object_counter}_"
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
            C.getFrame(nm).setContact(True)
            C.getFrame(nm).setMass(self.per_cube_mass)

        obj_info = {
            "prefix": prefix,
            "file": str(gfile),
            "basename": os.path.basename(gfile),
            "spawn_xy": (x, y),
            "spawn_z": z,
            "theta_rad": theta,
            "theta_deg": float(np.degrees(theta)),
            "spawn_rect": rect,
            "alive": True,
            "spawn_half_mode": self.spawn_half_mode,
        }

        self.spawned_objects.append(obj_info)
        self.used_files.add(str(gfile))
        placed_rects.append(rect)

        return obj_info

    def spawn_voxels_best_effort(self, C: ry.Config, target_count):
        """
        Try to spawn up to target_count voxel objects.
        Prefer unused voxel files first for variety.
        """
        scene_rects = self._scene_occupied_rects(C)
        placed_rects = list(scene_rects)

        all_files = self._load_voxel_files()
        usable_files = [f for f in all_files if str(f) not in self.reserved_files]

        unused_files = [f for f in usable_files if str(f) not in self.used_files]
        already_used_files = [f for f in usable_files if str(f) in self.used_files]
        candidate_files = unused_files + already_used_files

        candidate_files = list(candidate_files)
        self.rng.shuffle(candidate_files)

        spawned = []
        attempted = set()

        while len(spawned) < target_count:
            found_one = False

            for gfile in candidate_files:
                gfile_str = str(gfile)
                if gfile_str in attempted:
                    continue

                obj = self._spawn_one_voxel(C, gfile_str, placed_rects)
                attempted.add(gfile_str)

                if obj is not None:
                    spawned.append(obj)
                    found_one = True
                    break

            if not found_one:
                break

        return spawned

    # =========================================================
    # Physics simulation
    # =========================================================
    def run_physx(self, C: ry.Config, sim_seconds=7.0, sim_dt=0.01):
        """Run PhysX simulation for the current config."""
        S = ry.Simulation(C, ry.SimulationEngine.physx, verbose=0)
        S.pushConfigToSim()

        steps = int(np.ceil(sim_seconds / sim_dt))
        for _ in range(steps):
            S.step([], sim_dt, ry.ControlMode.none)

        del S

    # =========================================================
    # On-table checking / removal
    # =========================================================
    def _is_object_on_table(self, C: ry.Config, obj, xy_margin=0.01, z_tolerance=0.15):
        """
        Check whether an object's base frame is still considered on the table.

        Note:
        This checks against the full table, not only the chosen spawn half.
        So the half restriction is only for spawning, not for final validity.
        """
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
        """
        Split alive objects into on_table and off_table.
        Returns (on_table, off_table).
        """
        off_table = []
        on_table = []

        for obj in self.spawned_objects:
            if not obj["alive"]:
                continue

            if self._is_object_on_table(C, obj, xy_margin=xy_margin, z_tolerance=z_tolerance):
                on_table.append(obj)
            else:
                off_table.append(obj)

        return on_table, off_table

    def remove_objects(self, C: ry.Config, objects_to_remove):
        """Delete all frames belonging to the given objects."""
        frame_names = set(C.getFrameNames())

        for obj in objects_to_remove:
            prefix = obj["prefix"]
            matching = [nm for nm in frame_names if nm.startswith(prefix)]

            for nm in sorted(matching, reverse=True):
                if nm in C.getFrameNames():
                    C.delFrame(nm)

            obj["alive"] = False

    # =========================================================
    # Full generation
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
        add_target_surface=True,
    ):
        """
        Main generation function.

        Returns
        -------
        (C, summary)
            C : ry.Config
                Final cleaned scene.

            summary : dict
                Metadata, including:
                - target_voxel_file
                - target_voxel_basename
                - target_surface_frame_name
                - target_surface_frame_names
        """
        C = self._load_base_scene()
        self._reset_tracking()

        target_spawned = 0

        # -----------------------------------------------------
        # Target-marker pipeline
        # -----------------------------------------------------
        if add_target_surface:
            voxel_file, cubes, surface = self._choose_target_voxel_and_side()

            print("Chosen target voxel:", os.path.basename(voxel_file))
            print("Chosen target side:", surface["side_name"])
            print("Voxel spawn half mode:", self.spawn_half_mode)
            print("Marker half mode:", self._opposite_half_mode(self.spawn_half_mode))

            surface_info = self._place_target_surface_marker(C)
            print("Placed target surface:")
            print(surface_info)

            target_obj = self.spawn_target_voxel(C)
            if target_obj is not None:
                target_spawned = 1

                # Reserve target file so clutter spawning does not reuse it
                self.reserved_files.add(self.target_voxel_file)

                print(f"Spawned target voxel: {target_obj['basename']}")
            else:
                print("Warning: Could not spawn target voxel.")

        # -----------------------------------------------------
        # Initial clutter spawn
        # -----------------------------------------------------
        remaining_to_spawn = max(0, num_voxels - target_spawned)
        initial_spawn_count = min(batch_spawn_count, remaining_to_spawn)

        initially_spawned = self.spawn_voxels_best_effort(C, initial_spawn_count)
        print(f"Initially spawned extra voxels: {len(initially_spawned)} / {initial_spawn_count}")

        # -----------------------------------------------------
        # Refill loop
        # -----------------------------------------------------
        round_idx = 0
        while True:
            round_idx += 1
            print(f"\n=== Simulation round {round_idx} ===")

            self.run_physx(C, sim_seconds=sim_seconds, sim_dt=sim_dt)

            on_table, off_table = self.find_objects_off_table(
                C,
                xy_margin=xy_margin,
                z_tolerance=z_tolerance,
            )

            print(f"On table: {len(on_table)} | Off table: {len(off_table)} | Target: {num_voxels}")

            if len(on_table) >= num_voxels:
                print("Desired number of voxels is on the table.")
                break

            if round_idx >= max_refill_rounds:
                print("Reached max refill rounds.")
                break

            if off_table:
                self.remove_objects(C, off_table)

            missing = num_voxels - len(on_table)
            to_spawn_now = min(batch_spawn_count, missing)

            print(f"Trying to respawn up to {to_spawn_now} voxel(s)...")
            spawned_now = self.spawn_voxels_best_effort(C, to_spawn_now)
            print(f"Respawned {len(spawned_now)} voxel(s).")

            if len(spawned_now) == 0:
                print("Could not spawn any new voxel this round. Stopping early.")
                break

        # -----------------------------------------------------
        # Final cleanup
        # -----------------------------------------------------
        # This is the key fix: even if the loop stops, the last scene may still
        # contain off-table objects. We remove them before returning.
        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        if final_off:
            print(f"Removing {len(final_off)} final off-table voxel(s) from returned config.")
            self.remove_objects(C, final_off)

        # Recompute after cleanup so summary matches the actual returned config
        final_on, final_off = self.find_objects_off_table(
            C,
            xy_margin=xy_margin,
            z_tolerance=z_tolerance,
        )

        summary = {
            "target": num_voxels,
            "final_on_table": len(final_on),
            "final_off_table": len(final_off),
            "rounds": round_idx,
            "batch_spawn_count": batch_spawn_count,
            "spawn_half_mode": self.spawn_half_mode,
            "marker_half_mode": self._opposite_half_mode(self.spawn_half_mode),
            "objects": self.spawned_objects,
            "target_surface": self.target_surface_info,
            "target_voxel_file": self.target_voxel_file,
            "target_voxel_basename": (
                os.path.basename(self.target_voxel_file)
                if self.target_voxel_file is not None else None
            ),
            "target_surface_frame_name": (
                self.target_surface_info["marker_frame_name"]
                if self.target_surface_info is not None else None
            ),
            "target_surface_frame_names": (
                self.target_surface_info["marker_tile_names"]
                if self.target_surface_info is not None else []
            ),
        }

        return C, summary

    # =========================================================
    # Save
    # =========================================================
    def save_environment(self, C: ry.Config, file_name="generated_panda_table_voxel_clutter.g"):
        """Save config C to a .g file and return the path."""
        out_file = self.output_dir / file_name
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(C.write())
        print("Saved:", out_file)
        return str(out_file)