import json
import os
from pathlib import Path

import bpy


def main():
    glb_path = Path(os.environ["SF_GLB_PATH"]).resolve()
    result_path = Path(os.environ.get("SF_FRESH_IMPORT_RESULT", "output/fresh-import.json")).resolve()
    result_path.parent.mkdir(parents=True, exist_ok=True)

    if not glb_path.is_file() or glb_path.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty GLB: {glb_path}")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(glb_path))

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    joint_count = sum(len(obj.data.bones) for obj in armatures)

    result = {
        "status": "success",
        "source": glb_path.name,
        "mesh_objects": len(meshes),
        "armatures": len(armatures),
        "joint_count": joint_count,
    }

    if len(meshes) < 1:
        raise RuntimeError("Fresh-imported GLB contains no mesh object")
    if len(armatures) < 1:
        raise RuntimeError("Fresh-imported GLB contains no armature")
    if joint_count != 53:
        raise RuntimeError(f"Expected 53 imported rig joints, got {joint_count}")

    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("IANEO Spatial Forge fresh-import PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
