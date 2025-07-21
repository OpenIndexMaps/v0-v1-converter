# OpenIndexMaps v0 to v1 Converter

This script converts GeoJSON files adhering to the OpenIndexMaps specification version 0.0.0 to version 1.0.0.

## Features

- Converts field names according to the v0-to-v1 crosswalk
- Preserves all unmapped fields
- Automatically sets missing required v1 fields (`available`, `websiteUrl`) to `null`
- Optional validation of output against the v1.0.0 JSON Schema
- Schema file path can be customized with a command-line argument

## Requirements

- Python 3.7+
- Optional: `jsonschema` (for schema validation)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python oim_v0_to_v1_converter.py INPUT_FILE.geojson [OUTPUT_FILE.geojson] [--validate] [--schema PATH_TO_SCHEMA]
```

### Arguments

- `INPUT_FILE.geojson`: Required. Path to the input file in v0 format.
- `OUTPUT_FILE.geojson`: Optional. Output file path. Defaults to `*_v1.geojson`.
- `--validate`: Optional. Validates the output against the schema file.
- `--schema`: Optional. Path to a schema JSON file. Defaults to `1.0.0.schema.json` located in the same directory as the script.

## Example

```bash
python oim_v0_to_v1_converter.py ny-aerial-photos-1980.geojson --validate
```

## Output

- Prints warnings to stdout for missing crosswalked fields (which are set to `null`)
- Writes the v1.0.0-formatted GeoJSON to the output file
- Validates the output against the schema (if `--validate` is specified)