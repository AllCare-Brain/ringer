# Testing
Purpose: This page describes validation patterns for reliability, checks, and score pathways.

## Test strata
- Unit-like tests in `tests/test_*` for run model, engine mocks, and parser behavior.
- Integration-style checks that exercise CLI flows and command pipelines.
- Mock worker fixtures in `engines/mock_worker.py` for deterministic engine behavior.

## Relevant files
- `tests/test_launcher.py`
- `tests/test_active_runs.py`
- `tests/test_lint.py`
- `tests/test_model_log.py`
- `tests/test_hud_server.py`

## Expected outcomes
- Lint errors should be attributable to specific manifest fields.
- Run artifacts should include identity, score, and verification outputs for dashboard rendering.
- HUD server tests should preserve endpoint contract stability for polling consumers.
