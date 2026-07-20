# Maintainers
Purpose: This page lists maintainer-facing guidance and recent contributor context.

## Current contributor context
- Active non-bot contributor observed from git history: Jonathan Edwards.
- Bot identity present in history: `allcare-brain-atlas[bot]` (excluded from contributor statements).

## Operational expectations
- Prefer small scoped changes with tests.
- Preserve existing run compatibility for dashboards and HUD.
- Update templates and registry files together when model routing behavior changes.

## Runtime touchpoints to monitor
- `ringer.py` for orchestration regressions.
- `registry/model-identity.toml` for model display or default changes.
- `dashboard/` and `hud/` for monitoring regressions.
