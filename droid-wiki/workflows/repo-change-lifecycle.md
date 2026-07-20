# Repository Change Lifecycle
Purpose: This page maps the expected process for code changes that impact runtime behavior.

Active contributors: Jonathan Edwards

## Lifecycle stages
- Discover: read docs and relevant source files.
- Implement: patch targeted modules.
- Validate: update/add tests in `tests/`.
- Document: adjust templates/manifest docs if behavior changes.

## Evidence paths
- Runtime behavior changes in `ringer.py` should be paired with `tests/test_lint.py` and related unit/integration tests.
- UI-facing changes should include `dashboard/` and/or `hud/` companion updates.
