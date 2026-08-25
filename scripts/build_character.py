import importlib
import json
import math
import os
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Vector


CONTROL_NAMES = ("gender", "age", "muscle", "weight", "height", "proportions")


def find_mpfb_module():
    """Return the loaded MPFB extension root module without assuming repository namespace."""
    for module_name in list(sys.modules):
        if module_name.endswith(".mpfb"):
            return importlib.import_module(module_name)
    try:
        return importlib.import_module("bl_ext.blender_org.mpfb")
    except ModuleNotFoundError as exc:
        raise RuntimeError("MPFB extension is not loaded") from exc


def dynamic_import(package_suffix: str, symbol: str):
    for module_name in list(sys.modules):
        if module_name.endswith(package_suffix):
            module = importlib.import_module(module_name)
            if not hasattr(module, symbol):
                raise AttributeError(f"{module_name} has no symbol {symbol}")
            return getattr(module, symbol)
    raise RuntimeError(f"MPFB module not loaded: *{package_suffix}")


def version_string(version):
    return ".".join(str(part) for part in version)


def load_manifest(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))

    expected_root = {"schema_version", "character_id", "version", "generator", "phenotype"}
    if set(data) != expected_root:
        extra = sorted(set(data) - expected_root)
        missing = sorted(expected_root - set(data))
        raise ValueError(f"Manifest root fields mismatch; extra={extra}, missing={missing}")
    if data["schema_version"] != "1.0":
        raise ValueError("Unsupported character manifest schema_version")
    if not isinstance(data["character_id"], str) or not data["character_id"]:
        raise ValueError("character_id must be a non-empty string")
    if not isinstance(data["version"], int) or isinstance(data["version"], bool) or data["version"] < 1:
        raise ValueError("version must be an integer >= 1")
    if data["generator"] != {"engine": "mpfb"}:
        raise ValueError("generator must be exactly {'engine': 'mpfb'}")

    phenotype = data["phenotype"]
    if not isinstance(phenotype, dict) or set(phenotype) != set(CONTROL_NAMES):
        raise ValueError(f"phenotype must contain exactly: {', '.join(CONTROL_NAMES)}")
    for name in CONTROL_NAMES:
        value = phenotype[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"phenotype.{name} must be numeric")
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"phenotype.{name} must be within 0.0..1.0")
        phenotype[name] = float(value)

    return data


def look_at(obj, target: Vector):
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def world_bounds(obj):
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    xs = [v.x for v in corners]
    ys = [v.y for v in corners]
    zs = [v.z for v in corners]
    return Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))


def add_neutral_material(obj):
    material = bpy.data.materials.new("GenericHumanMaterial")
    material.diffuse_color = (0.58, 0.38, 0.28, 1.0)
    material.roughness = 0.72
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


def add_light(name, location, energy, size):
    data = bpy.data.lights.new(name=name, type="AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    return obj


def render_view(scene, camera, target, location, path):
    camera.location = location
    look_at(camera, target)
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def inspect_glb(path: Path):
    with path.open("rb") as handle:
        header = handle.read(12)
        if len(header) != 12:
            raise RuntimeError("GLB is too small")
        magic, glb_version, total_length = struct.unpack("<4sII", header)
        if magic != b"glTF" or glb_version != 2 or total_length != path.stat().st_size:
            raise RuntimeError("Invalid GLB header")
        chunk_length, chunk_type = struct.unpack("<II", handle.read(8))
        if chunk_type != 0x4E4F534A:
            raise RuntimeError("First GLB chunk is not JSON")
        payload = handle.read(chunk_length).decode("utf-8").rstrip(" \t\r\n\x00")
        document = json.loads(payload)

    skins = document.get("skins", [])
    joint_count = sum(len(skin.get("joints", [])) for skin in skins)
    return {
        "mesh_count": len(document.get("meshes", [])),
        "skin_count": len(skins),
        "joint_count": joint_count,
    }


def output_entry(kind, path: Path):
    return {"kind": kind, "path": path.name, "bytes": path.stat().st_size}


def main():
    manifest_path = Path(os.environ.get("SF_MANIFEST", "fixtures/generic-character-v1.json")).resolve()
    output_dir = Path(os.environ.get("SF_OUTPUT_DIR", "output/character-manifest")).resolve()
    expected_mpfb = os.environ.get("SF_EXPECTED_MPFB_VERSION", "2.0.17")
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(manifest_path)
    mpfb = find_mpfb_module()
    actual_mpfb = version_string(mpfb.VERSION)
    if actual_mpfb != expected_mpfb:
        raise RuntimeError(
            f"MPFB runtime drift: expected {expected_mpfb}, installed {actual_mpfb}. "
            "Do not silently continue with an unverified extension version."
        )

    HumanService = dynamic_import("mpfb.services.humanservice", "HumanService")
    TargetService = dynamic_import("mpfb.services.targetservice", "TargetService")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    macro = TargetService.get_default_macro_info_dict()
    for name in CONTROL_NAMES:
        macro[name] = manifest["phenotype"][name]

    human = HumanService.create_human(scale=0.1, feet_on_ground=True, macro_detail_dict=macro)
    human.name = f"{manifest['character_id']}_v{manifest['version']}"
    add_neutral_material(human)

    rig = HumanService.add_builtin_rig(human, "game_engine")
    if rig is None:
        raise RuntimeError("MPFB failed to create game_engine rig")
    rig.name = f"{human.name}_rig"

    bbox_min, bbox_max = world_bounds(human)
    center = (bbox_min + bbox_max) * 0.5
    height = bbox_max.z - bbox_min.z
    width = max(bbox_max.x - bbox_min.x, bbox_max.y - bbox_min.y)
    distance = max(height * 1.7, width * 3.5)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.035, 0.035, 0.045)

    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 58
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera

    key = add_light(
        "Key",
        (center.x - height * 0.7, center.y - distance * 0.55, center.z + height * 0.6),
        950,
        max(height * 0.75, 1.0),
    )
    look_at(key, center)
    fill = add_light(
        "Fill",
        (center.x + height * 0.8, center.y - distance * 0.25, center.z + height * 0.2),
        500,
        max(height * 0.9, 1.0),
    )
    look_at(fill, center)

    stem = f"{manifest['character_id']}-v{manifest['version']}"
    blend_path = output_dir / f"{stem}.blend"
    glb_path = output_dir / f"{stem}.glb"
    front_path = output_dir / "front.png"
    three_quarter_path = output_dir / "three-quarter.png"
    result_path = output_dir / "build-result.json"

    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    bpy.ops.object.select_all(action="DESELECT")
    human.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.export_scene.gltf(filepath=str(glb_path), export_format="GLB", use_selection=True)

    front_location = Vector((center.x, center.y - distance, center.z + height * 0.02))
    render_view(scene, camera, center, front_location, front_path)

    angle = math.radians(35)
    three_quarter_location = Vector((
        center.x + math.sin(angle) * distance,
        center.y - math.cos(angle) * distance,
        center.z + height * 0.02,
    ))
    render_view(scene, camera, center, three_quarter_location, three_quarter_path)

    structural = inspect_glb(glb_path)
    result = {
        "schema_version": "1.0",
        "character_id": manifest["character_id"],
        "version": manifest["version"],
        "status": "success",
        "runtime": {
            "blender": bpy.app.version_string,
            "mpfb": actual_mpfb,
        },
        "applied_controls": dict(manifest["phenotype"]),
        "unsupported_fields": [],
        "outputs": [
            output_entry("blend", blend_path),
            output_entry("glb", glb_path),
            output_entry("preview", front_path),
            output_entry("preview", three_quarter_path),
        ],
        "structural": structural,
        "visual_evidence": [front_path.name, three_quarter_path.name],
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("IANEO Spatial Forge manifest build PASS")
    print("Manifest:", manifest_path)
    print("Blender:", bpy.app.version_string)
    print("MPFB:", actual_mpfb)
    print("Applied controls:", result["applied_controls"])
    print("Structural:", structural)
    print("Output:", output_dir)


if __name__ == "__main__":
    main()
