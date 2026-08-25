import importlib
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def dynamic_import(package_suffix: str, symbol: str):
    """Resolve MPFB symbols from Blender's extension module namespace."""
    for module_name in list(sys.modules):
        if module_name.endswith(package_suffix):
            module = importlib.import_module(module_name)
            if not hasattr(module, symbol):
                raise AttributeError(f"{module_name} has no symbol {symbol}")
            return getattr(module, symbol)
    raise RuntimeError(f"MPFB module not loaded: *{package_suffix}")


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


def main():
    output_dir = Path(os.environ.get("SF_OUTPUT_DIR", "output")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("IANEO Spatial Forge MPFB human proof")
    print("Blender:", bpy.app.version_string)
    print("Output:", output_dir)

    HumanService = dynamic_import("mpfb.services.humanservice", "HumanService")
    TargetService = dynamic_import("mpfb.services.targetservice", "TargetService")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    macro = TargetService.get_default_macro_info_dict()
    macro["gender"] = 1.0
    macro["age"] = 0.36
    macro["muscle"] = 0.72
    macro["weight"] = 0.48
    macro["height"] = 0.62
    macro["proportions"] = 0.58

    human = HumanService.create_human(
        scale=0.1,
        feet_on_ground=True,
        macro_detail_dict=macro,
    )
    human.name = "GenericHuman"
    add_neutral_material(human)

    rig = HumanService.add_builtin_rig(human, "game_engine")
    if rig is None:
        raise RuntimeError("MPFB failed to create game_engine rig")
    rig.name = "GenericHumanRig"

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

    blend_path = output_dir / "generic-human.blend"
    glb_path = output_dir / "generic-human.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    bpy.ops.object.select_all(action="DESELECT")
    human.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        use_selection=True,
    )

    front_location = Vector((center.x, center.y - distance, center.z + height * 0.02))
    render_view(scene, camera, center, front_location, output_dir / "front.png")

    angle = math.radians(35)
    three_quarter_location = Vector((
        center.x + math.sin(angle) * distance,
        center.y - math.cos(angle) * distance,
        center.z + height * 0.02,
    ))
    render_view(scene, camera, center, three_quarter_location, output_dir / "three-quarter.png")

    print("Human object:", human.name)
    print("Rig object:", rig.name)
    print("Rig bones:", len(rig.data.bones))
    print("Bounds min:", tuple(round(v, 4) for v in bbox_min))
    print("Bounds max:", tuple(round(v, 4) for v in bbox_max))
    print("Generated:", blend_path.name, glb_path.name, "front.png", "three-quarter.png")


if __name__ == "__main__":
    main()
