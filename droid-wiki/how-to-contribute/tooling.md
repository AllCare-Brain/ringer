# Tooling
Purpose: This page lists local and repo-managed tooling that supports development and verification.

## Mandatory tools
- Python test runner for `tests/`.
- Rust/Tauri toolchain when working on `hud/`.
- Existing shell wrappers in `engines/` and scripts in `scripts/`.

## Repo tooling
- `engines/opencode-sandboxed.sh`: command isolation wrapper for OpenCode execution.
- `engines/mock_worker.py`: deterministic worker for test simulation.
- `scripts/backfill_model_from_logs.py` and `scripts/backfill_model_log.py`: history repair helpers.
- `hud/sync-dist.sh` (referenced by `hud/README.md`) is the build-side asset sync path.

## Useful run points
- `./ringer.py catalog` to inspect supported catalogs.
- `./ringer.py models` to inspect model identity and capability surfaces.
- `./ringer.py db` for runtime DB-ish reads used by dashboards.
