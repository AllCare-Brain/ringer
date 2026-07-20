# Dashboard APIs
Purpose: This page maps the run visibility endpoints and views that depend on them.

Active contributors: Jonathan Edwards

## Runtime contract
The CLI serves dashboard data used by:
- `dashboard/dashboard.html`
- `dashboard/ringside.html`
- Tauri HUD backend polling

## Key endpoints and consumers
- State endpoints for active runs and task rows.
- Artifact endpoints for scores and identity.
- Log endpoints for error/details surfacing.

## Key references
- `ringer.py` endpoint handlers
- `dashboard/dashboard.html`
- `dashboard/ringside.html`
- `hud/src/main.rs`

## Layout notes
- API shape is expected to remain backward-compatible with existing tests (`tests/test_hud_server.py`, `tests/test_hud_single_tab.py`).
