# Manifest Schema Module
Purpose: This page documents the manifest structure and validation constraints.

Active contributors: Jonathan Edwards

## File touch points
- Manifest models in `ringer.py`.
- Template manifests under `templates/*/manifest.json`.

## Core schema concepts
- Task metadata and type
- Check definitions and command bindings
- Output file expectations
- Steering and model fields

## Enforcement behavior
- `./ringer.py lint` is the canonical validator.
- Failing templates in required shape are rejected before execution.

## Directory layout table
| File type | Source |
|---|---|
| Schema source | `ringer.py` |
| Runtime manifests | `templates/*/manifest.json` |
| Check skeletons | `templates/*/checks/*` |
