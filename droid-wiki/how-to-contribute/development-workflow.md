# Development Workflow
Purpose: This page defines the expected local iteration loop for feature and infrastructure work.

## Local workflow
1. Read target source page and related manifests.
2. Make scoped code change.
3. Add/adjust tests under `tests/`.
4. Keep changes under the same feature boundary unless refactor is explicit.
5. Confirm lint or test command for area if applicable.

## Common commands
- `./ringer.py lint <manifest>.json`
- `./ringer.py run <manifest>.json`
- `pytest` (repo-level test runs are available but not required for every change scope)

## File touch etiquette
- Keep UI assets in source location (`dashboard/`, `hud/frontend/`) and avoid editing generated artifacts.
- Keep check scripts meaningful and failing correctly.
- Route new kit behavior through `templates/*/manifest.json` + checks, not through ad hoc orchestration bypasses.
