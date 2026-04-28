from __future__ import annotations

import hashlib
import os
import re
import shutil
import tempfile
import uuid
from pathlib import Path

import robotic as ry


_FRAME_RE = re.compile(
    r"^\s*([A-Za-z0-9_]+)(?:\(([^)]*)\))?\s*(?::)?\s*\{(.*?)\}\s*$",
    re.MULTILINE,
)
_MESH_RE = re.compile(r"\bmesh\s*:\s*(?:<([^>]+)>|'([^']+)'|\"([^\"]+)\")")
_SIZE_RE = re.compile(r"\bsize\s*:\s*\[(.*?)\]")
_MESHSCALE_RE = re.compile(r"\bmeshscale\s*:\s*(?:\[\s*(.*?)\s*\]|([^\s,}]+))")
_POSE_RE = re.compile(r"\bpose\s*:\s*\[(.*?)\]")
_X_RE = re.compile(r'\bX\s*:\s*"([^"]+)"')
_COLOR_RE = re.compile(r"\bcolor\s*:\s*\[(.*?)\]")
_CONTACT_RE = re.compile(r"\bcontact\s*:\s*([^\s,}]+)")
_MASS_RE = re.compile(r"\bmass\s*:\s*([^\s,}]+)")
_INERTIA_RE = re.compile(r"\binertia\s*:\s*\[(.*?)\]")
_WORLD_T_RE = re.compile(r"t\(\s*([^\)]+)\)")
_SCALAR_MESHSCALE_RE = re.compile(
    r"(\bmeshscale\s*:\s*)(?!\[)([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
)


def _resolve_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def _resolve_scene_mesh_path(scene_path: Path, mesh_raw: str) -> Path:
    mesh_path = Path(os.path.expandvars(mesh_raw)).expanduser()
    if mesh_path.is_absolute():
        return mesh_path.resolve(strict=False)

    primary = (scene_path.parent / mesh_path).resolve(strict=False)
    if primary.exists():
        return primary

    module_dir = Path(__file__).resolve().parent
    trimmed_parts = list(mesh_path.parts)
    while trimmed_parts and trimmed_parts[0] in {".", ".."}:
        trimmed_parts.pop(0)

    if trimmed_parts:
        repo_relative = (module_dir / Path(*trimmed_parts)).resolve(strict=False)
        if repo_relative.exists():
            return repo_relative

    return primary


def _pick_group(match: re.Match[str] | None) -> str | None:
    if match is None:
        return None
    for group in match.groups():
        if group is not None:
            return group
    return None


def _parse_float_list(raw: str | None) -> list[float]:
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",")]
    out: list[float] = []
    for part in parts:
        if not part:
            continue
        out.append(float(part))
    return out


def _parse_scalar(raw: str | None, default=None):
    if raw is None:
        return default
    return float(raw.strip())


def _parse_scale(body: str) -> float:
    size_vals = _parse_float_list(_pick_group(_SIZE_RE.search(body)))
    if size_vals:
        return size_vals[0]

    meshscale_match = _MESHSCALE_RE.search(body)
    if meshscale_match:
        meshscale_raw = meshscale_match.group(1) or meshscale_match.group(2)
        meshscale_vals = _parse_float_list(meshscale_raw)
        if meshscale_vals:
            return meshscale_vals[0]
        scalar = _parse_scalar(meshscale_raw)
        if scalar is not None:
            return scalar

    return 1.0


def _parse_pose(body: str) -> tuple[list[float] | None, list[float] | None]:
    pose_match = _POSE_RE.search(body)
    if pose_match:
        pose = _parse_float_list(pose_match.group(1))
        if len(pose) == 3:
            return pose, None
        if len(pose) == 7:
            return pose[:3], pose[3:]

    x_match = _X_RE.search(body)
    if x_match:
        x_raw = x_match.group(1)
        t_match = _WORLD_T_RE.search(x_raw)
        if t_match:
            pos = [float(v) for v in t_match.group(1).split()]
            if len(pos) == 3:
                return pos, None

    return None, None


def _parse_scene_entries(scene_file: str | Path) -> list[dict[str, object]]:
    scene_path = _resolve_path(scene_file)
    text = scene_path.read_text()

    entries: list[dict[str, object]] = []

    for frame_name, parent_name, body in _FRAME_RE.findall(text):
        mesh_raw = _pick_group(_MESH_RE.search(body))
        if mesh_raw is None:
            continue

        pos, quat = _parse_pose(body)
        color = _parse_float_list(_pick_group(_COLOR_RE.search(body)))
        inertia_vals = _parse_float_list(_pick_group(_INERTIA_RE.search(body)))
        contact = _parse_scalar(_pick_group(_CONTACT_RE.search(body)))
        mass = _parse_scalar(_pick_group(_MASS_RE.search(body)))

        entries.append(
            {
                "frame": frame_name,
                "parent": parent_name.strip() if parent_name else "",
                "mesh_path": _resolve_scene_mesh_path(scene_path, mesh_raw),
                "scale": _parse_scale(body),
                "position": pos,
                "quaternion": quat,
                "color": color if color else None,
                "contact": int(contact) if contact is not None else None,
                "mass": mass,
                "inertia": inertia_vals if inertia_vals else None,
            }
        )

    return entries


def _sanitize_scene_text_for_addfile(text: str) -> str:
    """
    Normalize a few scalar forms that some `robotic` builds reject when loading
    a full `.g` file via `C.addFile(...)`.

    In particular, mesh frames written by `C.write()` may contain:

      meshscale: 0.00201356

    while `C.addFile(...)` expects array syntax:

      meshscale: [0.00201356]
    """
    return _SCALAR_MESHSCALE_RE.sub(r"\1[\2]", text)


def _drop_scaled_mesh_frames_for_addfile(text: str) -> str:
    """
    Remove mesh frames that declare `meshscale` before passing the scene through
    `C.addFile(...)`.

    Those frames are the ones we intend to recreate manually anyway, and some
    `robotic` builds fail on their `meshscale` representation during full-scene
    parsing. Keeping them out of `addFile(...)` lets us still restore the robot,
    table, joints, and other non-problematic frames from the `.g`.
    """

    def _replace(match: re.Match[str]) -> str:
        body = match.group(3)
        has_mesh = _MESH_RE.search(body) is not None
        has_meshscale = _MESHSCALE_RE.search(body) is not None
        if has_mesh and has_meshscale:
            return ""
        return match.group(0)

    return _FRAME_RE.sub(_replace, text)


def _cache_busted_mesh_path(mesh_path: Path, cache_root: Path) -> Path:
    """
    Mirror the mesh asset directory into a unique temp location so `robotic`
    loads it under a fresh mesh-path cache key.

    This avoids stale native mesh/texture cache entries within a long-lived
    notebook kernel when the same absolute mesh path was previously loaded with
    the wrong texture state.
    """
    mesh_path = mesh_path.resolve()
    src_dir = mesh_path.parent
    digest = hashlib.sha1(str(src_dir).encode("utf-8")).hexdigest()[:12]
    dst_dir = cache_root / f"{src_dir.name}_{digest}"

    if not dst_dir.exists():
        shutil.copytree(src_dir, dst_dir)

    return dst_dir / mesh_path.name


def _load_plain_mesh_geometry(mesh_path: Path, scale: float) -> tuple:
    """
    Load mesh geometry through `setMeshFile(...)` on a temporary frame and
    immediately extract only vertices/triangles so the caller can rebuild a
    plain non-textured mesh with `setMesh(...)`.
    """
    tmp = ry.Config()
    fr = tmp.addFrame("tmp_mesh_geom")
    fr.setMeshFile(str(mesh_path), scale=float(scale))
    verts = fr.getMeshPoints()
    tris = fr.getMeshTriangles()
    return verts, tris


def recreate_scene_from_g(
    scene_file: str | Path = "my_scene.g",
    cache_bust_mesh_paths: bool = True,
    cache_root: str | Path | None = None,
):
    """
    Recreate a scene from a .g file while preserving non-mesh scene state such
    as the robot, table, joints, and other base-scene frames.

    We first load the full `.g` file via `C.addFile(...)` so all non-mesh
    frames and current scene state are restored. Then we replace only the mesh
    frames by parsing their frame data and calling `addFrame` / `setMeshFile`
    directly, instead of trusting `C.addFile(...)` for textured mesh state.

    We keep `cd_into_mesh_files=False` and pass absolute mesh paths so objects
    with reused OBJ/MTL/PNG basenames across folders do not collide in the
    native asset cache.

    If `cache_bust_mesh_paths=True`, each mesh is loaded from a mirrored temp
    directory. This forces `robotic` to create fresh native mesh cache entries
    even when the same mesh path was previously loaded incorrectly in the same
    Python kernel.
    """

    ry.params_add({"cd_into_mesh_files": False})

    scene_path = _resolve_path(scene_file)
    scene_text = scene_path.read_text()
    sanitized_scene_text = _drop_scaled_mesh_frames_for_addfile(
        _sanitize_scene_text_for_addfile(scene_text)
    )
    scene_entries = _parse_scene_entries(scene_path)

    created: list[dict[str, object]] = []
    cache_root_path = (
        _resolve_path(cache_root)
        if cache_root is not None
        else Path(tempfile.gettempdir()) / "robotic_mesh_scene_cache"
    )
    cache_root_path.mkdir(parents=True, exist_ok=True)
    call_cache_root = cache_root_path / f"reload_{uuid.uuid4().hex}"
    call_cache_root.mkdir(parents=True, exist_ok=True)

    C = ry.Config()
    if sanitized_scene_text != scene_text:
        sanitized_scene_path = scene_path.parent / (
            f".{scene_path.stem}.sanitized.{uuid.uuid4().hex}{scene_path.suffix}"
        )
        try:
            sanitized_scene_path.write_text(sanitized_scene_text)
            C.addFile(str(sanitized_scene_path))
        finally:
            sanitized_scene_path.unlink(missing_ok=True)
    else:
        C.addFile(str(scene_path))

    mesh_frame_names = [entry["frame"] for entry in scene_entries]
    for frame_name in mesh_frame_names:
        if frame_name in C.getFrameNames():
            C.delFrame(frame_name)

    for entry in scene_entries:
        parent_name = str(entry["parent"]).strip()
        if parent_name and parent_name in C.getFrameNames():
            frame = C.addFrame(entry["frame"], parent=parent_name)
        else:
            frame = C.addFrame(entry["frame"])

        if entry["position"] is not None:
            frame.setPosition(entry["position"])
        if entry["quaternion"] is not None:
            frame.setQuaternion(entry["quaternion"])

        mesh_path = Path(entry["mesh_path"])
        load_mesh_path = (
            _cache_busted_mesh_path(mesh_path, call_cache_root)
            if cache_bust_mesh_paths
            else mesh_path
        )

        should_force_plain_goal_pose_mesh = (
            str(entry["frame"]).startswith("goal_pose_")
            and entry["color"] is not None
        )

        if should_force_plain_goal_pose_mesh:
            verts, tris = _load_plain_mesh_geometry(
                load_mesh_path,
                float(entry["scale"]),
            )
            frame.setMesh(verts, tris)
        else:
            frame.setMeshFile(str(load_mesh_path), scale=float(entry["scale"]))

        if entry["color"] is not None:
            frame.setColor(entry["color"])

        if entry["contact"] is not None:
            frame.setContact(int(entry["contact"]))

        if entry["mass"] is not None:
            inertia = entry["inertia"] if entry["inertia"] is not None else []
            frame.setMass(float(entry["mass"]), inertia)

        created.append(
            {
                **entry,
                "loaded_mesh_path": load_mesh_path,
            }
        )

    return C, created
