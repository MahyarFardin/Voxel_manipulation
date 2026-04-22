from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import robotic as ry

from rebuild_scene_from_g import _sanitize_scene_text_for_addfile

_FRAME_LINE_RE = re.compile(
    r"(^\s*([A-Za-z0-9_]+)(?:\([^)]*\))?\s*:\s*\{)(.*?)(\}\s*$)",
    re.MULTILINE,
)
_MESH_RE = re.compile(r"\bmesh\s*:\s*<([^>]+)>")
_MESHSCALE_RE = re.compile(r"\bmeshscale\s*:\s*(?:\[\s*([^\]]+?)\s*\]|([^\s,}]+))")
_CACHE_MESH_PATH_RE = re.compile(
    r"/tmp/robotic_mesh_(?:live|scene)_cache/(?:live|reload)_[^/]+/([^/_][^/]*)_[0-9a-f]+/([^>]+)"
)

_MODULE_DIR = Path(__file__).resolve().parent
_DEFAULT_MESH_DATASET_DIR = _MODULE_DIR / "mesh_dataset"


def _norm_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def _rai_root() -> Path:
    return _norm_path(ry.raiPath(""))


def _relative_mesh_path_for_save(
    mesh_path: str | Path,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> str:
    raw_path = str(mesh_path)
    dataset_dir = _norm_path(dataset_dir)
    if raw_path.startswith("$RAI_PATH/"):
        return raw_path

    cache_match = _CACHE_MESH_PATH_RE.search(raw_path)
    if cache_match:
        object_dir, mesh_name = cache_match.groups()
        candidate = dataset_dir / object_dir / mesh_name
        return Path(os.path.relpath(candidate, start=out_dir)).as_posix()

    resolved = _norm_path(raw_path)
    try:
        relative_to_dataset = resolved.relative_to(dataset_dir)
        return Path(os.path.relpath(dataset_dir / relative_to_dataset, start=out_dir)).as_posix()
    except ValueError:
        pass

    try:
        relative_to_rai = resolved.relative_to(_rai_root())
        return f"$RAI_PATH/{relative_to_rai.as_posix()}"
    except ValueError:
        pass

    return Path(os.path.relpath(resolved, start=out_dir)).as_posix()


def _rewrite_mesh_paths_in_scene_text(
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> str:
    def _replace(match: re.Match[str]) -> str:
        saved_mesh_path = _relative_mesh_path_for_save(
            match.group(1),
            out_dir=out_dir,
            dataset_dir=dataset_dir,
        )
        return f"mesh: <{saved_mesh_path}>"

    return _MESH_RE.sub(_replace, scene_text)

def _extract_meshscale(body: str) -> float | None:
    meshscale_match = _MESHSCALE_RE.search(body)
    if meshscale_match is None:
        return None
    raw_value = meshscale_match.group(1) or meshscale_match.group(2)
    if raw_value is None:
        return None
    try:
        return float(raw_value.strip())
    except ValueError:
        return None


def _goal_pose_metadata_from_spawned_objects(
    out_dir: Path,
    spawned_objects: Sequence[Mapping[str, object]],
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> dict[str, object] | None:
    goal_pose_objs = [
        obj
        for obj in spawned_objects
        if obj.get("alive") and obj.get("role") == "goal_pose"
    ]
    if len(goal_pose_objs) != 1:
        return None

    obj = goal_pose_objs[0]
    return {
        "frame_name": str(obj["frame_name"]),
        "mesh_path": _relative_mesh_path_for_save(
            obj["mesh_path"],
            out_dir=out_dir,
            dataset_dir=dataset_dir,
        ),
        "scale_factor": float(obj["scale_factor"]),
    }


def _goal_pose_metadata_from_goal_frame(
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> dict[str, object] | None:
    missing_goal_pose_names = _goal_pose_frames_missing_mesh_metadata(scene_text)
    if not missing_goal_pose_names:
        return None

    for match in _FRAME_LINE_RE.finditer(scene_text):
        frame_name = match.group(2)
        body = match.group(3)

        if (
            not frame_name.startswith("goal_")
            or frame_name.startswith("goal_pose_")
            or not frame_name.endswith("_mesh")
        ):
            continue

        mesh_match = _MESH_RE.search(body)
        scale_factor = _extract_meshscale(body)
        if mesh_match is None or scale_factor is None:
            continue

        return {
            "frame_name": missing_goal_pose_names[0],
            "mesh_path": _relative_mesh_path_for_save(
                mesh_match.group(1).strip(),
                out_dir=out_dir,
                dataset_dir=dataset_dir,
            ),
            "scale_factor": scale_factor,
        }

    return None


def _shared_goal_mesh_metadata(
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> dict[str, object] | None:
    for match in _FRAME_LINE_RE.finditer(scene_text):
        frame_name = match.group(2)
        body = match.group(3)

        if (
            not frame_name.startswith("goal_")
            or frame_name.startswith("goal_pose_")
            or not frame_name.endswith("_mesh")
        ):
            continue

        mesh_match = _MESH_RE.search(body)
        scale_factor = _extract_meshscale(body)
        if mesh_match is None or scale_factor is None:
            continue

        return {
            "mesh_path": _relative_mesh_path_for_save(
                mesh_match.group(1).strip(),
                out_dir=out_dir,
                dataset_dir=dataset_dir,
            ),
            "scale_factor": scale_factor,
        }

    return None


def _restore_goal_pose_mesh_metadata(
    scene_text: str,
    metadata: Mapping[str, object] | None,
) -> str:
    if metadata is None:
        return scene_text

    frame_name = str(metadata["frame_name"])
    save_mesh_path = str(metadata["mesh_path"])
    scale_factor = float(metadata["scale_factor"])

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


def _restore_all_goal_pose_mesh_metadata_from_goal_frame(
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> str:
    shared_goal_metadata = _shared_goal_mesh_metadata(
        scene_text,
        out_dir=out_dir,
        dataset_dir=dataset_dir,
    )
    if shared_goal_metadata is None:
        return scene_text

    missing_goal_pose_names = _goal_pose_frames_missing_mesh_metadata(scene_text)
    for frame_name in missing_goal_pose_names:
        scene_text = _restore_goal_pose_mesh_metadata(
            scene_text,
            {
                "frame_name": frame_name,
                "mesh_path": shared_goal_metadata["mesh_path"],
                "scale_factor": shared_goal_metadata["scale_factor"],
            },
        )

    return scene_text


def _goal_pose_frames_missing_mesh_metadata(scene_text: str) -> list[str]:
    missing: list[str] = []
    for match in _FRAME_LINE_RE.finditer(scene_text):
        frame_name = match.group(2)
        body = match.group(3)
        if not frame_name.startswith("goal_pose_") or not frame_name.endswith("_mesh"):
            continue
        if _MESH_RE.search(body) is None or _extract_meshscale(body) is None:
            missing.append(frame_name)
    return missing


def _scene_mesh_metadata_by_frame(
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> dict[str, dict[str, object]]:
    metadata: dict[str, dict[str, object]] = {}
    for match in _FRAME_LINE_RE.finditer(scene_text):
        frame_name = match.group(2)
        body = match.group(3)
        mesh_match = _MESH_RE.search(body)
        scale_factor = _extract_meshscale(body)
        if mesh_match is None or scale_factor is None:
            continue
        metadata[frame_name] = {
            "frame_name": frame_name,
            "mesh_path": _relative_mesh_path_for_save(
                mesh_match.group(1).strip(),
                out_dir=out_dir,
                dataset_dir=dataset_dir,
            ),
            "scale_factor": scale_factor,
        }
    return metadata


def _frame_mesh_signature(C: ry.Config, frame_name: str) -> tuple[int, int, tuple[float, ...]] | None:
    if frame_name not in C.getFrameNames():
        return None

    fr = C.getFrame(frame_name)
    try:
        verts = fr.getMeshPoints()
        tris = fr.getMeshTriangles()
    except Exception:
        return None

    if verts is None or tris is None or len(verts) == 0:
        return None

    verts_arr = np.asarray(verts, dtype=float)
    tris_arr = np.asarray(tris)
    extents = tuple(np.round(verts_arr.max(axis=0) - verts_arr.min(axis=0), 8).tolist())
    return (int(len(verts_arr)), int(len(tris_arr)), extents)


def _goal_pose_metadata_from_matching_mesh_frame(
    C: ry.Config,
    scene_text: str,
    out_dir: Path,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
) -> dict[str, object] | None:
    scene_mesh_by_frame = _scene_mesh_metadata_by_frame(
        scene_text,
        out_dir=out_dir,
        dataset_dir=dataset_dir,
    )
    if not scene_mesh_by_frame:
        return None

    goal_pose_names = _goal_pose_frames_missing_mesh_metadata(scene_text)
    if len(goal_pose_names) != 1:
        return None

    goal_pose_name = goal_pose_names[0]
    goal_pose_sig = _frame_mesh_signature(C, goal_pose_name)
    if goal_pose_sig is None:
        return None

    preferred_candidates: list[dict[str, object]] = []
    fallback_candidates: list[dict[str, object]] = []

    for candidate_frame_name, metadata in scene_mesh_by_frame.items():
        if candidate_frame_name == goal_pose_name or candidate_frame_name.startswith("goal_pose_"):
            continue

        candidate_sig = _frame_mesh_signature(C, candidate_frame_name)
        if candidate_sig != goal_pose_sig:
            continue

        record = {
            "frame_name": goal_pose_name,
            "mesh_path": metadata["mesh_path"],
            "scale_factor": metadata["scale_factor"],
            "source_frame_name": candidate_frame_name,
        }
        fallback_candidates.append(record)
        if candidate_frame_name.startswith("goal_"):
            preferred_candidates.append(record)

    if len(preferred_candidates) == 1:
        return preferred_candidates[0]
    if len(preferred_candidates) > 1:
        return None
    if len(fallback_candidates) == 1:
        return fallback_candidates[0]
    return None


def build_g_scene_text(
    C: ry.Config,
    output_path: str | Path,
    spawned_objects: Sequence[Mapping[str, object]] | None = None,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
    base_scene_file: str | Path | None = None,
) -> str:
    scene_text = C.write()
    out_file = Path(output_path)
    out_dir = out_file.parent.resolve(strict=False)
    spawned_objects = list(spawned_objects or [])

    for obj in spawned_objects:
        if not obj.get("alive"):
            continue

        loaded_mesh_path = str(obj.get("loaded_mesh_path", obj["mesh_path"]))
        save_mesh_path = _relative_mesh_path_for_save(
            obj["mesh_path"],
            out_dir=out_dir,
            dataset_dir=dataset_dir,
        )

        scene_text = scene_text.replace(loaded_mesh_path, save_mesh_path)
        scene_text = scene_text.replace(str(_norm_path(obj["mesh_path"])), save_mesh_path)

    scene_text = _rewrite_mesh_paths_in_scene_text(
        scene_text,
        out_dir=out_dir,
        dataset_dir=dataset_dir,
    )

    goal_pose_metadata = _goal_pose_metadata_from_spawned_objects(
        out_dir,
        spawned_objects,
        dataset_dir=dataset_dir,
    )
    if goal_pose_metadata is None:
        goal_pose_metadata = _goal_pose_metadata_from_goal_frame(
            scene_text,
            out_dir=out_dir,
            dataset_dir=dataset_dir,
        )
    if goal_pose_metadata is None:
        goal_pose_metadata = _goal_pose_metadata_from_matching_mesh_frame(
            C,
            scene_text,
            out_dir=out_dir,
            dataset_dir=dataset_dir,
        )

    scene_text = _restore_goal_pose_mesh_metadata(scene_text, goal_pose_metadata)
    scene_text = _restore_all_goal_pose_mesh_metadata_from_goal_frame(
        scene_text,
        out_dir=out_dir,
        dataset_dir=dataset_dir,
    )
    return _sanitize_scene_text_for_addfile(scene_text)


def save_config_as_g(
    C: ry.Config,
    output_path: str | Path,
    spawned_objects: Sequence[Mapping[str, object]] | None = None,
    dataset_dir: str | Path = _DEFAULT_MESH_DATASET_DIR,
    base_scene_file: str | Path | None = None,
) -> str:
    out_file = Path(output_path).expanduser()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    scene_text = build_g_scene_text(
        C,
        out_file,
        spawned_objects=spawned_objects,
        dataset_dir=dataset_dir,
        base_scene_file=base_scene_file,
    )
    out_file.write_text(scene_text, encoding="utf-8")

    print("Saved:", out_file)
    return str(out_file)
