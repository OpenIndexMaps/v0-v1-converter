# OpenIndexMaps v0 to v1 Converter

This script converts GeoJSON files adhering to the OpenIndexMaps specification version 0.0.0 to version 1.0.0.

## Features
- Converts and maps key fields:
  - `recordIdentifier` → `recId`
  - `downloadUrl` → `download`
  - `thumbnailUrl` → `thumbUrl`
  - `available` → `available`
  - `websiteUrl` → `websiteUrl`
- Preserves all other metadata properties.
- Automatically fills missing crosswalked fields with `null`, logging a warning.
- Skips features with schema-incompatible property keys.
- Optionally validates output using a local OIM v1.0.0 schema.

## Usage

```bash
python oim_v0_to_v1_converter.py input_file.json [output_file.json] [--validate] [--schema path/to/schema.json]
```

### Arguments
- `input_file.json`: Required. Path to input GeoJSON file using OIM v0.0.0.
- `output_file.json`: Optional. If omitted, defaults to `input_file_v1.json`.
- `--validate`: Optional. If set, the output will be validated against the JSON Schema.
- `--schema`: Optional. Path to a JSON Schema file. If not provided, defaults to `1.0.0.schema.json` located next to the script.

## Installation
Requires Python 3.10+.

Install the required dependency with:

```bash
pip install -r requirements.txt
```
