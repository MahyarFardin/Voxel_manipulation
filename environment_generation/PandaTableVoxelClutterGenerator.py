import os
from glob import glob
from pathlib import Path

import numpy as np
import robotic as ry


class PandaTableVoxelClutterGenerator:
    """
    PandaTableVoxelClutterGenerator
    ===============================

    High-level idea
    ---------------
    This class generates cluttered table scenes containing:
    1. A Panda robot and a table loaded from a base RAI scene.
    2. Multiple voxel objects loaded from pre-generated voxel .g files.
    3. Optionally, a colored target-surface marker placed on the table.
       This marker represents one stable resting face of one chosen voxel object.

    The goal is to create scenes where many voxel objects physically settle on the table,
    instead of simply placing them in final positions directly.

    ----------------------------------------------------------------------
    How the generation pipeline works
    ----------------------------------------------------------------------
    The overall generation process is:

    1. Load the base scene
       - Load the Panda + table scene from a .g file.
       - Resize / reposition the table and Panda base if desired.

    2. Optionally choose a "target voxel" and one stable resting side
       - A voxel file is chosen uniformly from those that have at least one stable resting face.
       - Then one stable face of that voxel is chosen uniformly.
       - A marker is placed on the table with the same footprint and colors as that support face.
       - Then that same voxel is spawned somewhere in the clutter.

    3. Spawn some additional voxel objects
       - Objects are spawned above the table with random XY location and random Z rotation.
       - They are not placed directly in final resting positions.
       - Instead, they are dropped from above and allowed to settle with physics.

    4. Run physics simulation
       - Some objects remain on the table.
       - Some may fall off the table or end up outside the valid region.

    5. Remove failed objects and refill missing ones
       - After simulation, we check which objects are still on the table.
       - Objects that fell off are deleted from the scene.
       - New objects are spawned to replace missing ones.

    6. Repeat until enough objects remain on the table
       - This continues for multiple rounds, up to a maximum number of refill rounds.

    ----------------------------------------------------------------------
    Why do we do multiple spawn / simulate / refill rounds?
    ----------------------------------------------------------------------
    If we only spawn all objects once, many of them may:
    - collide badly during falling,
    - get pushed off the table,
    - land outside the valid table area,
    - or create overly unstable clutter.

    Because of that, a single spawn pass often does not leave the desired number
    of objects on the table.

    So instead, the generator uses a best-effort iterative approach:
    - spawn some objects,
    - simulate,
    - remove the ones that failed,
    - respawn replacements,
    - simulate again.

    This makes the final scene much more robust, because the generator keeps trying
    until either:
    - the requested number of objects remain on the table, or
    - the maximum refill limit is reached.

    ----------------------------------------------------------------------
    Important concepts in the code
    ----------------------------------------------------------------------
    - "occupied rectangles":
        For spawning, each object is approximated by an XY rectangle on the table.
        This allows fast collision-free placement before physics starts.

    - "stable resting surface":
        For a given voxel shape, a face is considered stably restable if the projected
        center of mass lies inside the support polygon formed by the cubes touching that face.

    - "target surface marker":
        A thin colored patch placed on the table that visually represents the support
        footprint of one stable side of the chosen target voxel.

    - "reserved file":
        Once the target voxel file is chosen, it is reserved so that clutter spawning
        does not immediately reuse the same file unintentionally.

    Parameters
    ----------
    base_scene_file : str or Path
        Path to the base RAI scene file containing the Panda robot and the table.

    voxel_dir : str or Path
        Directory containing voxel .g files that will be used as clutter objects.

    output_dir : str or Path
        Directory where generated environment files will be saved.

    table_frame_name : str
        Name of the table frame inside the base scene.

    gap : float
        Minimum spacing margin used when placing voxel objects and marker regions in XY.

    spawn_height : float
        Extra vertical offset above the table from which objects are spawned before falling.

    seed : int
        Random seed for reproducibility.

    per_cube_mass : float
        Mass assigned to each cube frame of a voxel object for physics simulation.

    table_shape_size : tuple
        New size of the table frame, typically (x_size, y_size, z_size, rounding).

    panda_base_relative_pos : tuple
        Relative position assigned to frame 'l_panda_base'.

    marker_thickness : float
        Thickness of the thin target-surface tiles placed on the table.
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
    ):
        # Path to the base Panda+table scene
        self.base_scene_file = Path(base_scene_file)

        # Folder containing voxel .g files that define clutter objects
        self.voxel_dir = Path(voxel_dir)

        # Folder where final generated environments will be saved
        self.output_dir = Path(output_dir)

        # Name of the table frame in the loaded base scene
        self.table_frame_name = table_frame_name

        # Minimum extra spacing used between rectangles during XY placement
        self.gap = gap

        # Height above the table where an object is initially spawned before falling
        self.spawn_height = float(spawn_height)

        # Random seed for reproducibility
        self.seed = seed

        # Mass assigned to each cube in a voxel object during simulation
        self.per_cube_mass = per_cube_mass

        # New table size written into the base scene:
        # (x_size, y_size, z_size, rounding)
        self.table_shape_size = list(table_shape_size)

        # Position offset for the Panda base relative to its parent
        self.panda_base_relative_pos = list(panda_base_relative_pos)

        # Thickness of target-surface marker tiles placed on the table
        self.marker_thickness = float(marker_thickness)

        # Make sure the base scene exists
        if not self.base_scene_file.exists():
            raise FileNotFoundError(f"Base scene file not found: {self.base_scene_file}")

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Use NumPy random generator for controlled reproducibility
        self.rng = np.random.default_rng(self.seed)

        # Tracking for generated objects
        self.spawned_objects = []   # metadata for all spawned objects
        self.used_files = set()     # voxel files already used in spawning
        self.reserved_files = set() # voxel files that should be excluded from normal clutter spawning
        self.object_counter = 0     # unique counter for obj0_, obj1_, ...

        # Static occupied rectangles that should block new spawning
        # Example: the target marker footprint
        self.static_rects = []

        # Information about the chosen target surface / voxel
        self.target_surface_info = None
        self.target_voxel_file = None
        self.target_surface_choice = None

    # =========================================================
    # Basic helpers
    # =========================================================
    def _cube_frames(self, C: ry.Config, prefix: str):
        """
        Return all frame names in config C that:
        - start with the given prefix, and
        - contain 'cube' in the name.

        This is used to find the cube frames belonging to one voxel object.
        """
        return [n for n in C.getFrameNames() if n.startswith(prefix) and "cube" in n]

    def _quat_from_z_rotation(self, theta: float):
        """
        Create a quaternion for a pure rotation around the z-axis by angle theta.
        Quaternion format here is [w, x, y, z].

        This is used to randomly rotate voxel objects around the vertical axis.
        """
        return [float(np.cos(theta / 2.0)), 0.0, 0.0, float(np.sin(theta / 2.0))]

    def _load_voxel_files(self):
        """
        Load and return all voxel .g files from self.voxel_dir.

        Raises
        ------
        FileNotFoundError
            If no voxel files are found.
        """
        voxel_files = sorted(glob(str(self.voxel_dir / "*.g")))
        if not voxel_files:
            raise FileNotFoundError(f"No voxel files found in: {self.voxel_dir}")
        return voxel_files

    def _load_base_scene(self):
        """
        Load the base Panda scene, verify required frames, and apply:
        - table shape override
        - Panda base position override

        Returns
        -------
        ry.Config
            The initialized scene config.
        """
        C = ry.Config()
        C.addFile(str(self.base_scene_file))

        # Ensure the table exists
        if self.table_frame_name not in C.getFrameNames():
            raise ValueError(f"Table frame '{self.table_frame_name}' not found in scene.")

        # Ensure Panda base exists
        if "l_panda_base" not in C.getFrameNames():
            raise ValueError("Frame 'l_panda_base' not found in scene.")

        # Override the table geometry
        C.getFrame(self.table_frame_name).setShape(
            ry.ST.ssBox,
            self.table_shape_size
        )

        # Reposition Panda base if needed
        C.getFrame("l_panda_base").setRelativePosition(
            self.panda_base_relative_pos
        )

        return C

    # =========================================================
    # Scene geometry
    # =========================================================
    def _get_table_info(self, C: ry.Config):
        """
        Return useful information about the table:
        - frame object
        - center position
        - size
        - top z value

        Returns
        -------
        dict
            Contains:
            - frame
            - pos
            - size
            - top_z
        """
        if self.table_frame_name not in C.getFrameNames():
            raise ValueError(f"Table frame '{self.table_frame_name}' not found in scene.")

        table = C.getFrame(self.table_frame_name)
        table_pos = np.array(table.getPosition(), dtype=float)
        table_size = np.array(table.getSize(), dtype=float)

        if len(table_size) < 3:
            raise ValueError(f"Table frame '{self.table_frame_name}' does not have a valid box size.")

        tx, ty, tz = float(table_size[0]), float(table_size[1]), float(table_size[2])
        px, py, pz = float(table_pos[0]), float(table_pos[1]), float(table_pos[2])

        return {
            "frame": table,
            "pos": np.array([px, py, pz], dtype=float),
            "size": np.array([tx, ty, tz], dtype=float),
            "top_z": pz + tz / 2.0,
        }

    def _table_bounds_xy(self, C: ry.Config, margin=0.0):
        """
        Compute the valid XY bounds of the table.

        Parameters
        ----------
        margin : float
            Optional inward margin to shrink the usable area.

        Returns
        -------
        (xmin, xmax, ymin, ymax)
        """
        info = self._get_table_info(C)
        tx, ty, _ = info["size"]
        px, py, _ = info["pos"]

        xmin = px - tx / 2.0 + margin
        xmax = px + tx / 2.0 - margin
        ymin = py - ty / 2.0 + margin
        ymax = py + ty / 2.0 - margin
        return xmin, xmax, ymin, ymax

    def _voxel_cube_geometry(self, file_path: str):
        """
        Load a voxel .g file temporarily and extract per-cube geometry:
        - cube frame name
        - local position
        - size
        - color

        This does not yet place the object into the real scene. It is only used
        for geometry analysis, stable-face analysis, and spawn-size estimation.

        Returns
        -------
        list of dict
            One entry per cube.
        """
        T = ry.Config()
        T.addFile(file_path, namePrefix="tmp_")

        cube_names = self._cube_frames(T, "tmp_")
        if len(cube_names) == 0:
            raise ValueError(f"No cube frames found in {file_path}")

        cubes = []
        for nm in cube_names:
            fr = T.getFrame(nm)

            # Cube dimensions
            size = np.array(fr.getSize()[:3], dtype=float)

            # Cube center in local voxel coordinates
            pos = np.array(fr.getPosition(), dtype=float)

            # Default color in case color is not explicitly stored
            color = [0.8, 0.8, 0.8]

            # Try to read color from frame attributes
            try:
                attrs = fr.getAttributes()
                if "color" in attrs:
                    raw_color = list(attrs["color"])
                    if len(raw_color) >= 3:
                        color = [float(raw_color[0]), float(raw_color[1]), float(raw_color[2])]
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
        """
        Compute local axis-aligned bounding box (AABB) of a voxel object.

        Returns
        -------
        (min_corner, max_corner)
            3D corners of the bounding box in local coordinates.
        """
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
        Estimate the XY footprint size of a voxel after rotation by theta around z.

        We rotate each cube's XY rectangle corners and take the min/max across all cubes.

        Returns
        -------
        min_xy, max_xy, size_xy
            Rotated XY bounding box and its size.
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

            # Corners of this cube's XY box
            corners = np.array([
                [center_xy[0] - hx, center_xy[1] - hy],
                [center_xy[0] - hx, center_xy[1] + hy],
                [center_xy[0] + hx, center_xy[1] - hy],
                [center_xy[0] + hx, center_xy[1] + hy],
            ])

            # Rotate corners into the candidate object orientation
            rotated = corners @ R.T
            min_xy = np.minimum(min_xy, rotated.min(axis=0))
            max_xy = np.maximum(max_xy, rotated.max(axis=0))

        return min_xy, max_xy, (max_xy - min_xy)

    def _rectangles_overlap(self, rect1, rect2, extra_gap=0.0):
        """
        Check if two axis-aligned rectangles overlap in XY,
        optionally with an additional safety gap.

        Each rectangle is (xmin, xmax, ymin, ymax).
        """
        x1_min, x1_max, y1_min, y1_max = rect1
        x2_min, x2_max, y2_min, y2_max = rect2

        return not (
            x1_max + extra_gap <= x2_min or
            x2_max + extra_gap <= x1_min or
            y1_max + extra_gap <= y2_min or
            y2_max + extra_gap <= y1_min
        )

    # =========================================================
    # 2D geometry helpers for stability
    # =========================================================
    def _cross2d(self, o, a, b):
        """
        2D cross product sign for orientation testing.
        Used in convex hull construction and polygon checks.
        """
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _convex_hull_2d(self, points):
        """
        Compute 2D convex hull of a set of points using the monotonic chain algorithm.

        Returns
        -------
        list of (x, y)
            Hull vertices in order.
        """
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
        """
        Check whether point p lies on the line segment a-b.
        Used as a degenerate case in convex polygon tests.
        """
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
        """
        Check whether point p lies inside or on the boundary of a convex polygon.

        This is used to test stability:
        if the projected center of mass lies inside the support polygon,
        then that face is considered stably restable.
        """
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
        """
        Compute the approximate center of mass of the voxel object by treating
        each cube mass as proportional to its volume.

        Returns
        -------
        np.ndarray, shape (3,)
            COM in local voxel coordinates.
        """
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
        Analyze one candidate resting face of the voxel object.

        Parameters
        ----------
        cubes : list
            Cube geometry dictionaries.

        axis : int
            0 -> x face
            1 -> y face
            2 -> z face

        use_max_side : bool
            False -> negative face (-x / -y / -z)
            True  -> positive face (+x / +y / +z)

        Returns
        -------
        dict or None
            Detailed information about this candidate support face.
        """
        # The 2 axes that remain after projecting away the support axis
        other_axes = [ax for ax in [0, 1, 2] if ax != axis]

        # Determine which cubes touch the chosen outermost plane
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

        # Build support geometry in the 2D plane of contact
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

        # Convex hull of support contact corners
        hull = self._convex_hull_2d(corners)

        # Project global center of mass into that 2D support plane
        com = self._cube_com(cubes)
        com_proj = com[other_axes]

        # Stable if projected COM lies inside the support hull
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
        """
        Check all 6 axis-aligned outer faces of the voxel object and return
        those that are stable resting candidates.

        Returns
        -------
        list of dict
            Stable resting surface infos.
        """
        surfaces = []
        for axis in [0, 1, 2]:
            for use_max_side in [False, True]:
                info = self._resting_surface_info(cubes, axis, use_max_side)
                if info is not None and info["stable"]:
                    surfaces.append(info)
        return surfaces

    # =========================================================
    # Occupancy from existing scene
    # =========================================================
    def _frame_xy_rect(self, fr):
        """
        Approximate one frame by its XY bounding rectangle using frame size and position.

        Returns
        -------
        rect or None
            (xmin, xmax, ymin, ymax)
            Returns None if the frame does not have a valid size.
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
        Collect XY rectangles that are already occupying table space.

        Exclusions:
        - frames belonging to spawned voxel objects (obj*)
        - the table frame itself
        - target marker tiles (targetSurface_*)

        Why?
        Because when spawning new voxel objects, we want to treat static scene
        obstacles and marker footprints as occupied, but not double-count the
        already-tracked dynamic objects in the same way.

        Returns
        -------
        list of rectangles
        """
        rects = []
        names = C.getFrameNames()

        for nm in names:
            if nm.startswith("obj"):
                continue
            if nm == self.table_frame_name:
                continue
            if nm.startswith("targetSurface_"):
                continue

            fr = C.getFrame(nm)
            rect = self._frame_xy_rect(fr)
            if rect is None:
                continue

            xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=0.0)
            rxmin, rxmax, rymin, rymax = rect

            overlaps_table_xy = not (
                rxmax <= xmin or rxmin >= xmax or
                rymax <= ymin or rymin >= ymax
            )

            if overlaps_table_xy:
                rects.append(rect)

        # Add explicitly-tracked occupied regions such as marker footprints
        rects.extend(self.static_rects)
        return rects

    # =========================================================
    # Tracking
    # =========================================================
    def _reset_tracking(self):
        """
        Reset per-environment generation state before starting a fresh scene.
        """
        self.spawned_objects = []
        self.used_files = set()
        self.reserved_files = set()
        self.object_counter = 0
        self.static_rects = []
        self.target_surface_info = None
        self.target_voxel_file = None
        self.target_surface_choice = None

    # =========================================================
    # New target selection order:
    # 1) choose voxel uniformly from eligible voxels
    # 2) choose one stable side uniformly
    # 3) place sticker
    # 4) spawn same voxel
    # 5) fill clutter
    # =========================================================
    def _choose_target_voxel_and_side(self):
        """
        Choose:
        1. one voxel uniformly among voxel files that have at least one stable face,
        2. one stable face uniformly from that voxel.

        This ensures the target selection is not biased toward voxel files
        having many stable faces.

        Returns
        -------
        (voxel_file, cubes, surface)
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
        Place a thin colored marker on the table that matches the chosen target face.

        The marker is composed of one thin tile per touching support cube.
        These tiles preserve the footprint and color structure of the chosen face.

        Returns
        -------
        dict
            Metadata about the placed target surface marker.
        """
        if self.target_voxel_file is None or self.target_surface_choice is None:
            raise RuntimeError("Target voxel/side has not been chosen yet.")

        voxel_file = self.target_voxel_file
        surface = self.target_surface_choice

        # Marker size in XY is the bounding box of the chosen support face
        size_xy = surface["bbox_size_2d"]

        # Avoid placing marker on top of already occupied regions
        placed_rects = self._scene_occupied_rects(C)
        cx, cy, rect = self._sample_noncolliding_xy(C, size_xy, placed_rects)

        table_info = self._get_table_info(C)

        # Place marker slightly above the table top so it is visible
        z_marker = table_info["top_z"] + self.marker_thickness / 2.0

        # Center support tiles around the marker center
        local_center_2d = 0.5 * (surface["bbox_min_2d"] + surface["bbox_max_2d"])

        marker_prefix = "targetSurface_"
        tile_names = []

        for i, r in enumerate(surface["support_rects"]):
            # Convert local support tile coordinates into world table coordinates
            tile_center_local = r["center_2d"] - local_center_2d
            world_x = cx + float(tile_center_local[0])
            world_y = cy + float(tile_center_local[1])

            sx = float(r["size_2d"][0])
            sy = float(r["size_2d"][1])
            tile_color = [float(c) for c in r["color"][:3]]

            nm = f"{marker_prefix}tile_{i}"
            C.addFrame(nm) \
                .setShape(ry.ST.ssBox, size=[sx, sy, self.marker_thickness, 0.001]) \
                .setColor(tile_color) \
                .setPosition([world_x, world_y, z_marker])

            tile_names.append(nm)

        # Reserve the marker footprint so spawned objects do not overlap it
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
            "marker_tile_names": tile_names,
            "support_bbox_size_2d": surface["bbox_size_2d"].tolist(),
            "com_local": surface["com"].tolist(),
            "com_proj_local": surface["com_proj"].tolist(),
        }

        return self.target_surface_info

    def spawn_target_voxel(self, C: ry.Config):
        """
        Spawn the previously chosen target voxel into the scene.

        Returns
        -------
        dict or None
            Spawn metadata if successful, else None.
        """
        if self.target_voxel_file is None:
            raise RuntimeError("Target voxel file has not been selected yet.")

        placed_rects = self._scene_occupied_rects(C)
        obj = self._spawn_one_voxel(C, self.target_voxel_file, placed_rects)
        return obj

    # =========================================================
    # Spawning
    # =========================================================
    def _sample_noncolliding_xy(self, C: ry.Config, size_xy, placed_rects, max_tries=3000):
        """
        Sample a random XY position for a rectangle of size size_xy such that:
        - it lies fully inside the table bounds,
        - it does not overlap already occupied rectangles.

        Returns
        -------
        (x, y, rect)
            Center position and rectangle footprint.
        """
        xmin, xmax, ymin, ymax = self._table_bounds_xy(C, margin=0.0)

        half_x = size_xy[0] / 2.0
        half_y = size_xy[1] / 2.0

        x_min = xmin + half_x + self.gap
        x_max = xmax - half_x - self.gap
        y_min = ymin + half_y + self.gap
        y_max = ymax - half_y - self.gap

        if x_min > x_max or y_min > y_max:
            raise ValueError("Table too small for one of the rotated voxels.")

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

        raise RuntimeError("Could not find non-colliding spawn position.")

    def _spawn_one_voxel(self, C: ry.Config, gfile: str, placed_rects):
        """
        Spawn one voxel object into the scene:
        - compute its rotated XY footprint,
        - sample a valid non-overlapping XY position,
        - place it above the table,
        - enable physics and contact,
        - store tracking info.

        Returns
        -------
        dict or None
            Spawn metadata if successful, None if no valid placement was found.
        """
        cubes = self._voxel_cube_geometry(gfile)
        local_min, _ = self._local_aabb(cubes)

        # Random in-plane orientation
        theta = float(self.rng.uniform(0.0, 2.0 * np.pi))

        # Compute footprint after applying this random rotation
        _, _, rot_size_xy = self._rotated_xy_aabb_size(cubes, theta)

        try:
            x, y, rect = self._sample_noncolliding_xy(C, rot_size_xy, placed_rects)
        except RuntimeError:
            return None

        table_info = self._get_table_info(C)

        # Place object above the table so it can fall under physics
        z = float(table_info["top_z"] - local_min[2] + self.spawn_height)

        prefix = f"obj{self.object_counter}_"
        self.object_counter += 1

        # Add voxel frames into the real scene
        C.addFile(gfile, namePrefix=prefix)

        base = C.getFrame(f"{prefix}base")
        base.setAttributes({
            "multibody": True,
            "multibody_fixedBase": False,
            "multibody_gravity": True,
        })
        base.setPosition([x, y, z])
        base.setQuaternion(self._quat_from_z_rotation(theta))

        # Enable contact and mass for each cube in this voxel object
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
        }

        self.spawned_objects.append(obj_info)
        self.used_files.add(str(gfile))
        placed_rects.append(rect)

        return obj_info

    def spawn_voxels_best_effort(self, C: ry.Config, target_count):
        """
        Try to spawn up to target_count voxel objects.

        Strategy:
        - Prefer voxel files that have not been used yet.
        - Exclude reserved files (e.g. target voxel file after it is specially used).
        - Shuffle candidates for randomness.
        - Try files one by one until enough objects are spawned or no more fits are found.

        Returns
        -------
        list of dict
            Spawn metadata for successfully spawned objects.
        """
        scene_rects = self._scene_occupied_rects(C)
        placed_rects = list(scene_rects)

        all_files = self._load_voxel_files()
        usable_files = [f for f in all_files if str(f) not in self.reserved_files]

        # Prefer not-yet-used files first for variety
        unused_files = [f for f in usable_files if str(f) not in self.used_files]
        used_files = [f for f in usable_files if str(f) in self.used_files]
        candidate_files = unused_files + used_files

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
    # Simulation
    # =========================================================
    def run_physx(self, C: ry.Config, sim_seconds=7.0, sim_dt=0.01):
        """
        Run PhysX simulation for the current scene.

        Parameters
        ----------
        sim_seconds : float
            Total simulation duration.

        sim_dt : float
            Physics timestep.
        """
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
        Check whether the object's base frame is still considered on the table.

        Conditions:
        - base XY lies inside the table bounds (with optional margin),
        - base z is not too far below the table top.

        Returns
        -------
        bool
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
        Split currently alive spawned objects into:
        - on_table
        - off_table

        Returns
        -------
        (on_table, off_table)
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
        """
        Remove the frames belonging to the given objects from the scene
        and mark them as no longer alive.

        Parameters
        ----------
        objects_to_remove : list of dict
            Objects previously returned by spawn logic.
        """
        frame_names = set(C.getFrameNames())

        for obj in objects_to_remove:
            prefix = obj["prefix"]
            matching = [nm for nm in frame_names if nm.startswith(prefix)]

            # Delete in reverse order for safety
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

        Pipeline
        --------
        1. Load base scene and reset tracking.
        2. Optionally choose a target voxel + stable side and place target marker.
        3. Spawn the matching target voxel.
        4. Spawn some initial clutter objects.
        5. Repeatedly:
           - simulate physics,
           - remove off-table objects,
           - spawn replacements,
           until enough objects remain on the table or refill budget is exhausted.

        Parameters
        ----------
        num_voxels : int
            Desired final number of voxel objects on the table.

        sim_seconds : float
            Simulation duration per round.

        sim_dt : float
            Physics timestep.

        max_refill_rounds : int
            Maximum number of simulation/refill rounds.

        xy_margin : float
            Margin used when deciding whether objects are still on the table.

        z_tolerance : float
            Vertical tolerance for deciding whether an object has fallen off.

        batch_spawn_count : int
            Maximum number of objects to spawn in one refill batch.

        add_target_surface : bool
            Whether to place a target support marker and spawn the corresponding target voxel.

        Returns
        -------
        (C, summary)
            C : ry.Config
                Final generated scene.

            summary : dict
                Metadata about the generation process.
        """
        # Start from fresh base scene
        C = self._load_base_scene()
        self._reset_tracking()

        # Tracks whether the target voxel was successfully spawned
        target_spawned = 0

        # -----------------------------------------------------
        # Optional target-marker pipeline
        # -----------------------------------------------------
        if add_target_surface:
            voxel_file, cubes, surface = self._choose_target_voxel_and_side()

            print("Chosen target voxel:", os.path.basename(voxel_file))
            print("Chosen target side:", surface["side_name"])

            surface_info = self._place_target_surface_marker(C)
            print("Placed target surface:")
            print(surface_info)

            target_obj = self.spawn_target_voxel(C)
            if target_obj is not None:
                target_spawned = 1

                # Reserve target file so regular clutter spawning does not reuse it
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
        # Refill loop:
        # simulate -> remove fallen objects -> spawn replacements
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

            # Success condition
            if len(on_table) >= num_voxels:
                print("Desired number of voxels is on the table.")
                break

            # Stop condition: too many rounds
            if round_idx >= max_refill_rounds:
                print("Reached max refill rounds.")
                break

            # Remove failed objects before respawning
            if off_table:
                self.remove_objects(C, off_table)

            missing = num_voxels - len(on_table)
            to_spawn_now = min(batch_spawn_count, missing)

            print(f"Trying to respawn up to {to_spawn_now} voxel(s)...")
            spawned_now = self.spawn_voxels_best_effort(C, to_spawn_now)
            print(f"Respawned {len(spawned_now)} voxel(s).")

            # Stop early if no new object can be spawned
            if len(spawned_now) == 0:
                print("Could not spawn any new voxel this round. Stopping early.")
                break

        # Final bookkeeping
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
            "objects": self.spawned_objects,
            "target_surface": self.target_surface_info,
            "target_voxel_file": self.target_voxel_file,
        }

        return C, summary

    # =========================================================
    # Save
    # =========================================================
    def save_environment(self, C: ry.Config, file_name="generated_panda_table_voxel_clutter.g"):
        """
        Save the generated environment config to a .g file.

        Parameters
        ----------
        C : ry.Config
            Scene to save.

        file_name : str
            Name of the output .g file.

        Returns
        -------
        str
            Full saved file path.
        """
        out_file = self.output_dir / file_name
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(C.write())
        print("Saved:", out_file)
        return str(out_file)