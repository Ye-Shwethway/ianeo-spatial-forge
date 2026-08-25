from pathlib import Path
import os
import bpy


OUTPUT_DIR = Path(os.environ.get("SF_OUTPUT_DIR", "output")).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def create_scene() -> None:
    # Primary object
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 1.0))
    cube = bpy.context.active_object
    cube.name = "SpatialForgeCube"
    cube.scale = (1.0, 1.0, 1.0)

    material = bpy.data.materials.new(name="SpatialForgeMaterial")
    material.diffuse_color = (0.18, 0.42, 0.8, 1.0)
    cube.data.materials.append(material)

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=10.0, location=(0.0, 0.0, 0.0))
    floor = bpy.context.active_object
    floor.name = "Ground"

    floor_material = bpy.data.materials.new(name="GroundMaterial")
    floor_material.diffuse_color = (0.16, 0.16, 0.16, 1.0)
    floor.data.materials.append(floor_material)

    # Camera
    bpy.ops.object.camera_add(location=(5.5, -5.5, 4.5))
    camera = bpy.context.active_object
    camera.name = "Camera"
    bpy.context.scene.camera = camera

    direction = cube.location - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    # Key light
    bpy.ops.object.light_add(type="AREA", location=(4.0, -3.0, 6.0))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 900.0
    key.data.shape = "DISK"
    key.data.size = 5.0

    # Fill light
    bpy.ops.object.light_add(type="AREA", location=(-4.0, 1.5, 3.0))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 450.0
    fill.data.size = 4.0


def configure_render() -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = str(OUTPUT_DIR / "preview.png")


def save_outputs() -> None:
    blend_path = OUTPUT_DIR / "spatial-forge-smoke.blend"
    glb_path = OUTPUT_DIR / "spatial-forge-smoke.glb"

    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        export_apply=True,
    )
    bpy.ops.render.render(write_still=True)

    for path in (blend_path, glb_path, OUTPUT_DIR / "preview.png"):
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(f"Expected output missing or empty: {path}")
        print(f"OUTPUT {path.name} {path.stat().st_size} bytes")


if __name__ == "__main__":
    print("IANEO Spatial Forge Blender smoke test")
    print("Blender:", bpy.app.version_string)
    print("Output:", OUTPUT_DIR)
    reset_scene()
    create_scene()
    configure_render()
    save_outputs()
    print("SPATIAL_FORGE_SMOKE=PASS")
