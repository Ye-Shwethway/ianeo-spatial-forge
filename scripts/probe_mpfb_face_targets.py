import importlib
import json
import os
import sys
from pathlib import Path


def dynamic_import(package_suffix: str, symbol: str):
    for module_name in list(sys.modules):
        if module_name.endswith(package_suffix):
            module = importlib.import_module(module_name)
            if not hasattr(module, symbol):
                raise AttributeError(f"{module_name} has no symbol {symbol}")
            return getattr(module, symbol)
    raise RuntimeError(f"MPFB module not loaded: *{package_suffix}")


def find_mpfb_module():
    for module_name in list(sys.modules):
        if module_name.endswith(".mpfb"):
            return importlib.import_module(module_name)
    return importlib.import_module("bl_ext.blender_org.mpfb")


def main():
    expected = os.environ.get("SF_EXPECTED_MPFB_VERSION", "2.0.17")
    output = Path(os.environ.get("SF_FACE_TARGET_PROBE", "output/mpfb-face-targets.json")).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    mpfb = find_mpfb_module()
    actual = ".".join(str(part) for part in mpfb.VERSION)
    if actual != expected:
        raise RuntimeError(f"MPFB runtime drift: expected {expected}, got {actual}")

    LocationService = dynamic_import("mpfb.services.locationservice", "LocationService")
    target_json = Path(LocationService.get_mpfb_data("targets")) / "target.json"
    metadata = json.loads(target_json.read_text(encoding="utf-8"))

    keywords = (
        "head", "face", "forehead", "temple", "brow", "eyebrow", "eye", "eyelid",
        "cheek", "nose", "nostril", "mouth", "lip", "jaw", "chin", "ear",
    )
    records = []
    total = 0
    for section, section_data in metadata.items():
        for category in section_data.get("categories", []):
            category_name = category.get("name", "")
            for target_name in category.get("targets", []):
                total += 1
                haystack = f"{section} {category_name} {target_name}".lower()
                if any(keyword in haystack for keyword in keywords):
                    records.append({
                        "section": section,
                        "category": category_name,
                        "target": target_name,
                    })

    result = {
        "mpfb": actual,
        "target_catalog": str(target_json),
        "bundled_target_count": total,
        "face_candidate_count": len(records),
        "face_candidates": records,
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
