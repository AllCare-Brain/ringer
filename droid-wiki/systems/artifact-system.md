# Artifact System
Purpose: This page tracks how outputs, verification records, and identity evidence are written.

Active contributors: Jonathan Edwards

## Artifact categories
- Scorecard outputs
- Model and identity metadata
- Verification snapshots and check outcomes
- Task deliverable files in configured artifact directories

## Source files
| File | Role |
|---|---|
| `ringer.py` | Artifact generation logic |
| `templates/*` | Deliverable declarations |
| `tests/test_artifact_library.py` | Artifact collection expectations |

## Directory and schema expectations
- Artifact paths are task- and run-specific.
- Files named in checks are expected and validated.

## Entry points
- Extend artifact naming/fields in task manifest `expect_files` and core verification logic.
- Keep all artifacts machine-readable where dashboards consume them.
