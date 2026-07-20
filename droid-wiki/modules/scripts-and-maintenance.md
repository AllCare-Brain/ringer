# Scripts and Maintenance
Purpose: This page captures repo-level maintenance scripts for data correction and migration.

Active contributors: Jonathan Edwards

## Scripts in scope
- `scripts/backfill_model_from_logs.py`
- `scripts/backfill_model_log.py`

## Use cases
- Recover missing model identifiers in eval logs.
- Backfill legacy task types for compatibility with scoring views.

## Key behavior
- Preserve malformed lines and non-attributed rows.
- Add explicit notes when backfilled data is introduced (`model_backfill=command_log`).
- Use dry-run/backup behavior where offered to avoid irreversible changes.
