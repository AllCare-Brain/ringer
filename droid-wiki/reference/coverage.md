# Coverage and Skip Register
Purpose: This page records where source was mapped and where items are intentionally skipped.

## Covered non-trivial areas
- Core orchestrator (`ringer.py`)
- Engines and sandboxing (`engines/`)
- Templates and checks (`templates/`)
- Dashboard and HUD (`dashboard/`, `hud/`)
- Hooks and scripts (`hooks/`, `scripts/`)
- Registry and model references (`registry/`)
- Release and packaging (`.github/workflows/release.yml`)
- Test and verification suite (`tests/`)

## Skipped by design or status
- `__pycache__` directories (not source)
- Built artifacts in `hud/target` if present locally (tooling output)
- Archived or placeholder files under `droid-wiki/` are source of truth only after this generation step.
