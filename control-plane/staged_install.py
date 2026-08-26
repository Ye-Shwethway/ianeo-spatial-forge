import json
import shutil
from pathlib import Path

REQUIRED_FILES = (
    "model.glb",
    "build-result.json",
    "front.png",
    "three-quarter.png",
)


def _valid_build_id(build_id):
    return (
        isinstance(build_id, str)
        and bool(build_id)
        and "/" not in build_id
        and "\\" not in build_id
        and not build_id.startswith(".")
    )


def promote_staged_build(root):
    root = Path(root)
    stage = root / "app" / "build-staging" / "current"
    marker = stage / "install.json"
    if not marker.is_file():
        return None

    request = json.loads(marker.read_text(encoding="utf-8"))
    build_id = request.get("build_id")
    if not _valid_build_id(build_id):
        raise ValueError("invalid staged build_id")
    if stage.is_symlink():
        raise ValueError("staging directory must not be a symlink")

    for name in REQUIRED_FILES:
        source = stage / name
        if not source.is_file() or source.is_symlink() or source.stat().st_size <= 0:
            raise ValueError(f"missing or invalid staged asset: {name}")

    builds = root / "private" / "builds"
    builds.mkdir(parents=True, exist_ok=True)
    target = builds / build_id
    temporary = builds / f".{build_id}.installing"

    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir()
    for name in REQUIRED_FILES:
        shutil.copy2(stage / name, temporary / name)

    if target.exists():
        if target.is_symlink() or not target.is_dir():
            shutil.rmtree(temporary)
            raise ValueError("existing build target is invalid")
        shutil.rmtree(target)
    temporary.replace(target)
    return build_id
