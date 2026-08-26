import json
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_character as base


FACE_CONTROL_MAP = {
    "head_width": (("head-scale-horiz-decr",), ("head-scale-horiz-incr",)),
    "head_depth": (("head-scale-depth-decr",), ("head-scale-depth-incr",)),
    "cheek_bones": (
        ("l-cheek-bones-decr", "r-cheek-bones-decr"),
        ("l-cheek-bones-incr", "r-cheek-bones-incr"),
    ),
    "cheek_volume": (
        ("l-cheek-volume-decr", "r-cheek-volume-decr"),
        ("l-cheek-volume-incr", "r-cheek-volume-incr"),
    ),
    "chin_width": (("chin-width-decr",), ("chin-width-incr",)),
    "chin_height": (("chin-height-decr",), ("chin-height-incr",)),
    "chin_prominence": (("chin-prominent-decr",), ("chin-prominent-incr",)),
    "nose_width": (("nose-scale-horiz-decr",), ("nose-scale-horiz-incr",)),
    "nose_depth": (("nose-scale-depth-decr",), ("nose-scale-depth-incr",)),
    "eye_scale": (
        ("l-eye-scale-decr", "r-eye-scale-decr"),
        ("l-eye-scale-incr", "r-eye-scale-incr"),
    ),
    "eye_height": (
        ("l-eye-height2-decr", "r-eye-height2-decr"),
        ("l-eye-height2-incr", "r-eye-height2-incr"),
    ),
    "brow_angle": (("eyebrows-angle-down",), ("eyebrows-angle-up",)),
    "mouth_width": (("mouth-scale-horiz-decr",), ("mouth-scale-horiz-incr",)),
    "upper_lip_volume": (("mouth-upperlip-volume-decr",), ("mouth-upperlip-volume-incr",)),
    "lower_lip_volume": (("mouth-lowerlip-volume-decr",), ("mouth-lowerlip-volume-incr",)),
}


def load_face_profile(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"schema_version", "profile_id", "controls"}:
        raise ValueError("face profile must contain exactly schema_version, profile_id, controls")
    if data["schema_version"] != "1.0":
        raise ValueError("unsupported face profile schema_version")
    controls = data["controls"]
    if not isinstance(controls, dict) or not controls:
        raise ValueError("face controls must be a non-empty object")
    unknown = sorted(set(controls) - set(FACE_CONTROL_MAP))
    if unknown:
        raise ValueError(f"unsupported face controls: {unknown}")
    for name, value in controls.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"face control {name} must be numeric")
        value = float(value)
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"face control {name} must be within 0.0..1.0")
        controls[name] = value
    return data


def apply_face_profile(human, profile, TargetService):
    applied = []
    for control_name, value in profile["controls"].items():
        if abs(value - 0.5) < 1e-9:
            continue
        low_targets, high_targets = FACE_CONTROL_MAP[control_name]
        target_names = low_targets if value < 0.5 else high_targets
        weight = abs(value - 0.5) * 2.0
        for target_name in target_names:
            full_path = TargetService.target_full_path(target_name)
            if not full_path:
                raise RuntimeError(f"MPFB target not found: {target_name}")
            TargetService.load_target(human, full_path, weight=weight, name=target_name)
            applied.append({"control": control_name, "target": target_name, "weight": weight})
    bpy.context.view_layer.update()
    return applied


def apply_helper_masks(human):
    """Bake MPFB helper MASK modifiers so helper slabs cannot survive GLB export."""
    bpy.ops.object.select_all(action="DESELECT")
    human.hide_set(False)
    human.select_set(True)
    bpy.context.view_layer.objects.active = human

    mask_names = [modifier.name for modifier in human.modifiers if modifier.type == "MASK"]
    vertices_before = len(human.data.vertices)
    for modifier_name in mask_names:
        bpy.ops.object.modifier_apply(modifier=modifier_name)
    vertices_after = len(human.data.vertices)
    bpy.context.view_layer.update()

    return {
        "mask_modifiers_applied": mask_names,
        "vertices_before": vertices_before,
        "vertices_after": vertices_after,
    }


def main():
    manifest_path = Path(os.environ.get("SF_MANIFEST", "fixtures/generic-character-v1.json")).resolve()
    profile_path = Path(os.environ.get("SF_FACE_PROFILE", "fixtures/generic-face-quality-v1.json")).resolve()
    output_dir = Path(os.environ.get("SF_OUTPUT_DIR", "output/face-quality")).resolve()
    expected_mpfb = os.environ.get("SF_EXPECTED_MPFB_VERSION", "2.0.17")
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = base.load_manifest(manifest_path)
    profile = load_face_profile(profile_path)
    mpfb = base.find_mpfb_module()
    actual_mpfb = base.version_string(mpfb.VERSION)
    if actual_mpfb != expected_mpfb:
        raise RuntimeError(f"MPFB runtime drift: expected {expected_mpfb}, installed {actual_mpfb}")

    HumanService = base.dynamic_import("mpfb.services.humanservice", "HumanService")
    TargetService = base.dynamic_import("mpfb.services.targetservice", "TargetService")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    macro = TargetService.get_default_macro_info_dict()
    for name in base.CONTROL_NAMES:
        macro[name] = manifest["phenotype"][name]

    human = HumanService.create_human(
        scale=0.1,
        feet_on_ground=True,
        mask_helpers=True,
        detailed_helpers=True,
        extra_vertex_groups=True,
        macro_detail_dict=macro,
    )
    human.name = f"{manifest['character_id']}_{profile['profile_id']}"
    applied_targets = apply_face_profile(human, profile, TargetService)

    # Bake authored face targets first, then physically apply MPFB helper masks.
    # This keeps the intended body/face but removes helper geometry from render/export.
    TargetService.bake_targets(human)
    helper_cleanup = apply_helper_masks(human)
    base.add_neutral_material(human)

    rig = HumanService.add_builtin_rig(human, "game_engine")
    if rig is None:
        raise RuntimeError("MPFB failed to create game_engine rig")
    rig.name = f"{human.name}_rig"

    bbox_min, bbox_max = base.world_bounds(human)
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

    key = base.add_light(
        "Key",
        (center.x - height * 0.7, center.y - distance * 0.55, center.z + height * 0.6),
        950,
        max(height * 0.75, 1.0),
    )
    base.look_at(key, center)
    fill = base.add_light(
        "Fill",
        (center.x + height * 0.8, center.y - distance * 0.25, center.z + height * 0.2),
        500,
        max(height * 0.9, 1.0),
    )
    base.look_at(fill, center)

    stem = f"{manifest['character_id']}-{profile['profile_id']}"
    blend_path = output_dir / f"{stem}.blend"
    glb_path = output_dir / f"{stem}.glb"
    front_path = output_dir / "front.png"
    three_quarter_path = output_dir / "three-quarter.png"
    profile_render_path = output_dir / "profile.png"
    face_close_path = output_dir / "face-close.png"
    result_path = output_dir / "build-result.json"

    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    bpy.ops.object.select_all(action="DESELECT")
    human.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.export_scene.gltf(filepath=str(glb_path), export_format="GLB", use_selection=True)

    front_location = Vector((center.x, center.y - distance, center.z + height * 0.02))
    camera.data.lens = 58
    base.render_view(scene, camera, center, front_location, front_path)

    angle = math.radians(35)
    three_quarter_location = Vector((
        center.x + math.sin(angle) * distance,
        center.y - math.cos(angle) * distance,
        center.z + height * 0.02,
    ))
    base.render_view(scene, camera, center, three_quarter_location, three_quarter_path)

    profile_location = Vector((center.x + distance, center.y, center.z + height * 0.02))
    base.render_view(scene, camera, center, profile_location, profile_render_path)

    # Portrait evidence: deliberately head/shoulders dominant for face-form comparison.
    face_target = Vector((center.x, center.y, bbox_min.z + height * 0.895))
    camera.data.lens = 105
    face_distance = max(height * 0.25, width * 1.05)
    face_location = Vector((face_target.x, face_target.y - face_distance, face_target.z + height * 0.005))
    base.render_view(scene, camera, face_target, face_location, face_close_path)

    structural = base.inspect_glb(glb_path)
    result = {
        "schema_version": "1.0",
        "character_id": manifest["character_id"],
        "character_version": manifest["version"],
        "face_profile": profile,
        "runtime": {"blender": bpy.app.version_string, "mpfb": actual_mpfb},
        "locked_body_controls": dict(manifest["phenotype"]),
        "applied_face_targets": applied_targets,
        "helper_cleanup": helper_cleanup,
        "structural": structural,
        "visual_evidence": ["front.png", "three-quarter.png", "profile.png", "face-close.png"],
        "outputs": [
            base.output_entry("blend", blend_path),
            base.output_entry("glb", glb_path),
            base.output_entry("preview", front_path),
            base.output_entry("preview", three_quarter_path),
            base.output_entry("preview", profile_render_path),
            base.output_entry("preview", face_close_path),
        ],
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("IANEO Spatial Forge face quality build PASS")
    print("MPFB:", actual_mpfb)
    print("Face profile:", profile["profile_id"])
    print("Applied face targets:", len(applied_targets))
    print("Helper cleanup:", helper_cleanup)
    print("Structural:", structural)
    print("Output:", output_dir)


if __name__ == "__main__":
    main()
