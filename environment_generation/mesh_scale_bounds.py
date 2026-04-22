import json
import os

import numpy as np
import robotic as ry

ROOT_DIR = "mesh_dataset"
OUTPUT_JSON = "mesh_scaling_results_bounded.json"

# Mesh file extensions to try
MESH_EXTENSIONS = {".obj", ".ply", ".stl", ".off", ".dae", ".glb", ".gltf"}

# We keep the scaled minimum axis at or below this value.
TARGET_MIN_AXIS_MAX = 0.07

# We keep the scaled maximum axis strictly below this value.
TARGET_MAX_AXIS_STRICT = 0.3

# Tiny margin so the saved result stays strictly below TARGET_MAX_AXIS_STRICT.
STRICT_EPS = 1e-9


def is_mesh_file(filename):
    return os.path.splitext(filename)[1].lower() in MESH_EXTENSIONS


def compute_bounded_scale_for_mesh(
    mesh_path,
    target_min_axis_max=TARGET_MIN_AXIS_MAX,
    target_max_axis_strict=TARGET_MAX_AXIS_STRICT,
    strict_eps=STRICT_EPS,
):
    """
    Load a mesh, compute its AABB axis lengths, and return a scale factor that
    satisfies both of these constraints after scaling:

      - min(size_xyz * scale) <= target_min_axis_max
      - max(size_xyz * scale) < target_max_axis_strict

    The chosen scale is the largest scale that still satisfies both bounds, so
    the object is kept as large as possible without violating either one.
    """
    C = ry.Config()
    f = C.addFrame("tmp_mesh")

    # scale=1.0 so we measure the original mesh size
    f.setShape(ry.ST.mesh, size=1.0)
    f.setMeshFile(mesh_path, scale=1.0)

    V = f.getMeshPoints()
    if V is None or len(V) == 0:
        raise ValueError("Mesh has no vertices or could not be loaded.")

    V = np.asarray(V)
    mins = V.min(axis=0)
    maxs = V.max(axis=0)
    size_xyz = maxs - mins
    diag = np.linalg.norm(size_xyz)

    min_axis = float(np.min(size_xyz))
    max_axis = float(np.max(size_xyz))

    if min_axis <= 0 or max_axis <= 0:
        raise ValueError(f"Invalid mesh dimensions: {size_xyz}")

    max_scale_from_min = target_min_axis_max / min_axis
    strict_max_target = max(target_max_axis_strict - strict_eps, 0.0)
    max_scale_from_max = strict_max_target / max_axis

    scale = min(max_scale_from_min, max_scale_from_max)
    if scale <= 0:
        raise ValueError(
            "Could not compute a positive scale factor from the requested bounds."
        )

    return size_xyz, diag, scale


def scale_dataset_and_save_json(
    root_dir=ROOT_DIR,
    output_json=OUTPUT_JSON,
    target_min_axis_max=TARGET_MIN_AXIS_MAX,
    target_max_axis_strict=TARGET_MAX_AXIS_STRICT,
    strict_eps=STRICT_EPS,
):
    results = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not is_mesh_file(filename):
                continue

            mesh_path = os.path.join(dirpath, filename)

            try:
                size_xyz, diag, scale = compute_bounded_scale_for_mesh(
                    mesh_path,
                    target_min_axis_max=target_min_axis_max,
                    target_max_axis_strict=target_max_axis_strict,
                    strict_eps=strict_eps,
                )

                scaled_size_xyz = size_xyz * scale
                min_axis_after = float(np.min(scaled_size_xyz))
                max_axis_after = float(np.max(scaled_size_xyz))

                record = {
                    "mesh_path": mesh_path,
                    "aabb_size_xyz": size_xyz.tolist(),
                    "aabb_diagonal": float(diag),
                    "min_axis_before": float(np.min(size_xyz)),
                    "max_axis_before": float(np.max(size_xyz)),
                    "scale_factor": float(scale),
                    "aabb_size_xyz_after_scaling": scaled_size_xyz.tolist(),
                    "min_axis_after": min_axis_after,
                    "max_axis_after": max_axis_after,
                    "constraints": {
                        "min_axis_after_lte": float(target_min_axis_max),
                        "max_axis_after_lt": float(target_max_axis_strict),
                    },
                    "constraints_satisfied": (
                        min_axis_after <= target_min_axis_max
                        and max_axis_after < target_max_axis_strict
                    ),
                }
                results.append(record)

                print("=" * 80)
                print("Mesh:", mesh_path)
                print("AABB size xyz:", size_xyz)
                print("Diagonal:", diag)
                print("Scale factor:", scale)
                print("Scaled AABB xyz:", scaled_size_xyz)
                print("Scaled min axis:", min_axis_after)
                print("Scaled max axis:", max_axis_after)

            except Exception as e:
                print("=" * 80)
                print("Mesh:", mesh_path)
                print("ERROR:", e)

    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved results to {output_json}")
    return results


def main():
    scale_dataset_and_save_json()


if __name__ == "__main__":
    main()
