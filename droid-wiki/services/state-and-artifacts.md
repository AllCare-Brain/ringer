# State and Artifact Service
Purpose: This page documents run-state lifecycle and artifact persistence responsibilities.

Active contributors: Jonathan Edwards

## State model
- Run state files are authoritative for dashboard and HUD consumers.
- Task rows include status, key, model, and check outcomes.

## Artifact model
- Deliverables are validated by checks and expected file list.
- Score output and identity evidence are stored for consumption by dashboard and review surfaces.

## Source references
- `ringer.py`
- `tests/test_artifact_library.py`
- `tests/test_artifact_wrappers.py`
- `tests/test_scoreboard_page.py`

## Update points
- Add new artifact keys only through schema-consistent code and tests.
- Preserve backward compatibility for existing UI consumers.
