# Task and Runtime Model Module
Purpose: This page describes the datatypes used to represent tasks, engines, and runtime state.

Active contributors: Jonathan Edwards

## Core models
- `TaskSpec`
- `Manifest`
- `TaskRuntime`
- `WorkerResult`
- `VerifyResult`

## Source references
- `ringer.py`
- `tests/test_model_field.py`
- `tests/test_model_db.py`

## Extension points
- Add new task fields only with migration-safe defaults.
- Keep JSON output stable where dashboards and tests deserialize it.
