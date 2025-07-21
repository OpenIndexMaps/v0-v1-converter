import json
import argparse
from pathlib import Path
from copy import deepcopy

try:
    import jsonschema
except ImportError:
    jsonschema = None

# Crosswalk from v0 to v1 fields
CROSSWALK = {
    "recordIdentifier": "recId",
    "downloadUrl": "download",
    "thumbnailUrl": "thumbUrl",
    "available": "available",
    "websiteUrl": "websiteUrl",
}

def convert_feature(feature, feature_index):
    original_props = feature.get("properties", {})
    new_props = {}

    warnings = []

    # Copy original properties, skipping ones in CROSSWALK
    for k, v in original_props.items():
        if k not in CROSSWALK:
            new_props[k] = v

    # Crosswalk fields
    for v0_field, v1_field in CROSSWALK.items():
        if v0_field in original_props:
            new_props[v1_field] = original_props[v0_field]
        else:
            new_props[v1_field] = None
            warnings.append(f"Feature {feature_index}: missing '{v0_field}'; set '{v1_field}' to null")

    feature["properties"] = new_props
    return feature, warnings

def main():
    parser = argparse.ArgumentParser(description="Convert OpenIndexMaps v0 GeoJSON to v1.0.0")
    parser.add_argument("input", type=Path, help="Input GeoJSON file (v0)")
    parser.add_argument("output", type=Path, nargs="?", help="Output GeoJSON file (v1); defaults to *_v1.geojson")
    parser.add_argument("--validate", action="store_true", help="Validate output against v1 schema")
    parser.add_argument("--schema", type=Path, default=Path(__file__).parent / "1.0.0.schema.json",
                        help="Path to schema file (default: 1.0.0.schema.json in script directory)")

    args = parser.parse_args()

    with args.input.open() as f:
        data = json.load(f)

    output_path = args.output or args.input.with_name(args.input.stem + "_v1.geojson")

    output = {
        "type": "FeatureCollection",
        "features": [],
    }
    if "crs" in data:
        output["crs"] = data["crs"]

    skipped = 0
    total = 0

    for i, feature in enumerate(data.get("features", [])):
        total += 1
        new_feature, warnings = convert_feature(deepcopy(feature), i)
        for warning in warnings:
            print(warning)
        if new_feature is not None:
            output["features"].append(new_feature)
        else:
            skipped += 1

    with output_path.open("w") as f:
        json.dump(output, f, indent=2)

    print(f"\nConversion complete: {total - skipped} features written, {skipped} skipped")

    if args.validate:
        if jsonschema is None:
            print("\nERROR: jsonschema not installed. Run 'pip install jsonschema' to enable validation.")
            return
        try:
            with args.schema.open() as s:
                schema = json.load(s)
            jsonschema.validate(instance=output, schema=schema)
            print("Validation successful: output conforms to OIM v1 schema")
        except Exception as e:
            print(f"Validation failed: {e}")


if __name__ == "__main__":
    main()
