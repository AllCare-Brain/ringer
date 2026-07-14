# TRIP Failure/Recovery Smoke Receipt — 2026-07-14

PHI-free promotion smoke per lane section 13. All data synthetic. Result: pass.

## Gate conditions

| Condition | Evidence |
|---|---|
| Fails a check | Attempt 1 check exited 1: `simulated first-attempt check failure (smoke)`; failure text was injected into the retry prompt. |
| Consumes the native retry | Run summary: `implement-smoke-fail-recovery pass PASS attempts=2`, 81,115 tokens, 72.9s, engine `luna` (gpt-5.6-luna). |
| Resumes side effects mid-checkpoint-list | Release rehearsal: `commit` performed with SHA read-back, orchestrator interrupted, resume skipped the evidenced `commit` checkpoint and performed `push` then `tag`; remote head and tag read-back matched the local SHA. |

## Run identity

- `run_id`: `ope-305-trip-protocol-20260714T220400Z-p90861`
- `run_name`: `ope-305-trip-protocol` (OPE-305, phase `implement`, `plan_version` 2)
- Run log: `~/.ringer/runs/` (machine-local, per lane contract); artifact: Ringside `ope-305-trip-protocol`

## Validators executed

- `./ringer.py lint` — clean (1 task)
- `trip_contract.py manifest` — `PASS [manifest_contract]`
- `trip_contract.py release` — `PASS [release_contract]: 3 side effects pending` (verify command executed in the rehearsal repo)
- `python3 tests/test_trip_lifecycle.py` — 21/21 OK

## Defect found and fixed by this smoke

`trip_contract.py` invoked ringer via `sys.executable`, bypassing ringer's `#!/bin/sh` interpreter-selecting shebang; under a system Python older than 3.11 the lint verdict was a false FAIL. Fixed to execute the resolved ringer path directly; tests updated to stub ringer as an executable script.
