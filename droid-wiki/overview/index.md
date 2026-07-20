# Ringer Repository Overview
Purpose: This page summarizes what this repository is, how it is organized, and where major behavior lives.

## Purpose
Ringer is a local orchestration tool that runs task manifests through multiple AI engines, applies checks, and publishes structured artifacts such as manifests, deltas, models, and HUD dashboards.

## Repository map
| Top area | Purpose |
|---|---|
| `ringer.py` | Primary CLI and orchestration core |
| `dashboard/` | Web UIs for status, scores, and artifact views |
| `engines/` | Engine execution shims and sandbox wrappers |
| `hooks/` | Hook integration for proactive nudge checks |
| `hud/` | Native Tauri desktop mission-control app |
| `templates/` | Reusable manifest kits and checks |
| `registry/` | Model identity and capability registry files |
| `scripts/` | Migration and backfill scripts for historical logs |
| `tests/` | Acceptance and behavioral validation suite |
| `.github/workflows/` | Packaging/release for the HUD application |

## Key responsibilities
- Parse and validate manifest input.
- Normalize model selection and engine dispatch.
- Run worker rounds, collect results, and enforce checker behavior.
- Track run state and expose dashboard APIs.
- Score and verify outcomes into artifacts.
- Support local UI observability via web dashboard and desktop HUD.

## Entry points
- Primary CLI: `./ringer.py`.
- Local run: `./ringer.py run <manifest>`.
- Lint flow: `./ringer.py lint <manifest>`.
- Dashboard service: `./ringer.py dashboard`.
- HUD binary: `./hud/src-tauri` built via `cargo tauri build` inside `hud/`.

## Evidence-backed notes
- Manifest files are under `templates/*/manifest.json` and validated with `ringer.py lint`.
- Engine-specific behavior is implemented in `engines/` and executed by `RunPlan`/worker orchestration in `ringer.py`.
- Runtime state and logs are consumed by dashboard endpoints and HUD polling.
