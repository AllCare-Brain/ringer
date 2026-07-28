# Patterns and Conventions
Purpose: This page captures repeated implementation and manifest patterns used across the repo.

## Coding patterns
- Data classes and typed structs are used for manifest/runtime shape in `ringer.py`.
- Engine selection and fallback rules are centralized and not duplicated in check scripts.
- Logs and artifacts are treated as append-friendly records for reproducibility.

## Manifest conventions
- Keep manifest roles explicit: role, constraints, checks, expected outputs.
- Prefer explicit check failure messages over generic returns.
- For reusable behavior, add or update kits in `templates/` rather than embedding command chains ad hoc.

## Cross-cutting conventions
- Use dry-run and non-mutating paths where possible.
- Preserve existing state format compatibility.
- Keep dashboard-facing fields in sync with tests.
