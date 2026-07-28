# Debugging
Purpose: This page maps common debugging checkpoints when runs do not behave as expected.

## First checks
1. Confirm manifest lint passes before execution.
2. Verify engine is available and credentials are valid.
3. Check run-state JSON for task ordering and check statuses.
4. Inspect worker logs and command log lines used for model inference.

## Useful files
- `registry/model-identity.toml` when model display or routing looks wrong.
- `hooks/ringer_nudge.py` for pre/post tool hook behavior.
- `tests/test_log_endpoint.py` when troubleshooting run-state API surfaces.

## Common fixes
- Restore missing check outputs by tightening check command paths.
- If a run appears dead, confirm active-run bookkeeping cleanup and stale-process handling.
- For malformed JSON tool calls, consult tool-calling behavior notes in model capability files.
