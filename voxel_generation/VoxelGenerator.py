import os
import random
from glob import glob
from pathlib import Path

import numpy as np
import robotic as ry


class VoxelGenerator:
    def __init__(self, base_file="base.g", output_root="./data", step=0.1, default_size=0.1):
        self.base_file = Path(base_file)
        self.output_root = Path(output_root)
        self.step = step
        self.default_size = default_size

        if not self.base_file.exists():
            raise FileNotFoundError(f"Base file not found: {self.base_file}")

        self.output_root.mkdir(parents=True, exist_ok=True)

    def _random_color(self):
        return np.random.randint(0, 2, (3,)).tolist()

    def _load_base(self):
        return self.base_file.read_text(encoding="utf-8")

    def _generate_single_structure(self, color, n=None, size=None):
        """
        Creates the text of one .g file by adding random rigidly connected cubes.
        """
        if n is None:
            n = np.random.randint(1, 10)
        if size is None:
            size = self.default_size

        # Keep track of occupied voxel positions
        pixels = [[0.0, 0.0, 0.0]]
        base = self._load_base()

        for i in range(1, n):
            parent = random.choice(pixels)
            new_position = parent.copy()

            # Random walk until an unoccupied neighboring position is found
            while new_position in pixels:
                new_position = parent.copy()
                axis = np.random.randint(0, 3)
                direction = random.choice([-1, 1])
                new_position[axis] += direction * self.step

            base += f"""
joint{i}(cube{i-1}):{{
  joint: none,
  pre: "T t({parent[0]} {parent[1]} {parent[2]})"
}}

cube{i}(joint{i}):{{
  shape: box,
  size: [{size}, {size}, {size}],
  color: {color},
  position: [{new_position[0]}, {new_position[1]}, {new_position[2]}],
  X: "t({new_position[0]} {new_position[1]} {new_position[2]})"
}}
"""
            pixels.append(new_position)

        return base

    def generate_voxel_files(self, folder_name, num_voxels, n_range=(1, 10), size=None):
        """
        Generate multiple .g voxel files inside:
            output_root/folder_name/

        Args:
            folder_name (str): Name of the subfolder to save files into.
            num_voxels (int): Number of voxel .g files to generate.
            n_range (tuple): Range for random number of cubes, e.g. (1, 10).
            size (float): Cube size. If None, uses default_size.
        """
        target_folder = self.output_root / folder_name
        target_folder.mkdir(parents=True, exist_ok=True)

        created_files = []

        for i in range(num_voxels):
            n = np.random.randint(n_range[0], n_range[1])
            color = self._random_color()
            content = self._generate_single_structure(color=color, n=n, size=size)

            file_path = target_folder / f"voxel_{i:04d}.g"
            file_path.write_text(content, encoding="utf-8")
            created_files.append(str(file_path))

        print(f"Created {len(created_files)} voxel files in: {target_folder}")
        return created_files

    def visualize_folder(self, folder_name, spacing_low=1, spacing_high=10):
        """
        Visualize all .g files in output_root/folder_name by placing them at random offsets.
        """
        folder_path = self.output_root / folder_name
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        files = sorted(glob(str(folder_path / "*.g")))
        if not files:
            print(f"No .g files found in: {folder_path}")
            return

        C = ry.Config()
        p = np.array([0.0, 0.0, 0.0])

        for f in files:
            r = np.random.randint(spacing_low, spacing_high, (3,))
            C.addFile(f).setPosition((p + r).tolist())

        C.view(pause=True)
