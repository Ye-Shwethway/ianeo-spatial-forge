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
LOCKABLE_FIELDS = tuple(f"phenotype.{name}" for name in CONTROL_NAMES)
MEASUREMENT_UNITS = {"cm", "in", "kg", "lb", "percent"}
UNSUPPORTED_MEASUREMENT_REASON = (
    "MPFB 2.0.17 has no proven direct control that guarantees this exact real-world "
    "measurement; the request is preserved as intent and was not applied as an engine control."
)


def find_mpfb_module():
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

    required_root = {"schema_version", "character_id", "version", "generator", "phenotype"}
    allowed_root = required_root | {"requested_measurements", "revision"}
    extra = sorted(set(data) - allowed_root)
    missing = sorted(required_root - set(data))
    if extra or missing:
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

    revision = data.get("revision")
    if revision is not None:
        if not isinstance(revision, dict) or set(revision) != {"parent_version", "locked_fields"}:
            raise ValueError("revision must contain exactly parent_version and locked_fields")
        parent_version = revision["parent_version"]
        if not isinstance(parent_version, int) or isinstance(parent_version, bool) or parent_version < 1:
            raise ValueError("revision.parent_version must be an integer >= 1")
        locked_fields = revision["locked_fields"]
        if not isinstance(locked_fields, list) or len(locked_fields) != len(set(locked_fields)):
            raise ValueError("revision.locked_fields must be a unique array")
        unknown = sorted(set(locked_fields) - set(LOCKABLE_FIELDS))
        if unknown:
            raise ValueError(f"revision.locked_fields contains unsupported fields: {unknown}")

    requested_measurements = data.get("requested_measurements", [])
    if not isinstance(requested_measurements, list):
        raise ValueError("requested_measurements must be an array")
    for index, request in enumerate(requested_measurements):
        if not isinstance(request, dict) or set(request) != {"field", "value", "unit"}:
            raise ValueError(f"requested_measurements[{index}] must contain exactly field, value, unit")
        field = request["field"]
        if not isinstance(field, str) or not field or not field[0].isalpha() or not all(
            char.islower() or char.isdigit() or char == "_" for char in field
        ):
            raise ValueError(f"requested_measurements[{index}].field must be lower snake_case")
        value = request["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"requested_measurements[{index}].value must be numeric")
        request["value"] = float(value)
        if request["unit"] not in MEASUREMENT_UNITS:
            raise ValueError(f"requested_measurements[{index}].unit is unsupported")

    return data


def enforce_revision(manifest, parent_path):
    revision = manifest.get("revision")
    if revision is None:
        if parent_path:
            raise ValueError("SF_PARENT_MANIFEST was supplied but manifest has no revision block")
        return None
    if not parent_path:
        raise ValueError("revision manifest requires SF_PARENT_MANIFEST")

    parent = load_manifest(Path(parent_path).resolve())
    if parent["character_id"] != manifest["character_id"]:
        raise ValueError("revision parent character_id does not match")
    if parent["version"] != revision["parent_version"]:
        raise ValueError("revision parent_version does not match parent manifest version")
    if manifest["version"] <= parent["version"]:
        raise ValueError("revision version must be greater than parent version")

    for field in revision["locked_fields"]:
        _, name = field.split(".", 1)
        if manifest["phenotype"][name] != parent["phenotype"][name]:
            raise ValueError(
                f"locked field drift: {field} parent={parent['phenotype'][name]} "
                f"revision={manifest['phenotype'][name]}"
            )

    return {
        "parent_version": parent["version"],
        "locked_fields": list(revision["locked_fields"]),
    }


def unsupported_measurements(manifest):
    return [
        {
            "field": request["field"],
            "requested_value": request["value"],
            "unit": request["unit"],
            "reason": UNSUPPORTED_MEASUREMENT_REASON,
        }
        for request in manifest.get("requested_measurements", [])
    ]


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
    parent_manifest_path = os.environ.get("SF_PARENT_MANIFEST")
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(manifest_path)
    revision = enforce_revision(manifest, parent_manifest_path)
    unsupported = unsupported_measurements(manifest)
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
        "runtime": {"blender": bpy.app.version_string, "mpfb": actual_mpfb},
        "applied_controls": dict(manifest["phenotype"]),
        "unsupported_fields": unsupported,
        "outputs": [
            output_entry("blend", blend_path),
            output_entry("glb", glb_path),
            output_entry("preview", front_path),
            output_entry("preview", three_quarter_path),
        ],
        "structural": structural,
        "visual_evidence": [front_path.name, three_quarter_path.name],
    }
    if revision is not None:
        result["revision"] = revision
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("IANEO Spatial Forge manifest build PASS")
    print("Manifest:", manifest_path)
    print("Blender:", bpy.app.version_string)
    print("MPFB:", actual_mpfb)
    print("Applied controls:", result["applied_controls"])
    print("Revision:", revision)
    print("Unsupported measurements:", unsupported)
    print("Structural:", structural)
    print("Output:", output_dir)


if __name__ == "__main__":
    main()
