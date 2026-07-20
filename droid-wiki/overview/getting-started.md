# Getting Started
Purpose: This page gives the quickest path to run, inspect, and verify a Ringer cycle locally.

## Minimal prerequisites
- Python 3.11+
- Node/Rust toolchain only if building `hud/`
- Required engine auth configured in standard local environment (e.g., Codex/Grok/OpenRouter auth flow)
- Optional: HUD prerequisites from `hud/README.md`

## Common first run
1. Inspect help: `./ringer.py --help`.
2. Validate a manifest: `./ringer.py lint examples/manifest.json` (or any local manifest).
3. Start a run: `./ringer.py run <manifest>.json --name demo-run`.
4. Open local dashboard output in `dashboard/dashboard.html` or run HUD.

## Useful source files
- Entry CLI: `ringer.py`
- Example manifest shapes: `templates/*/manifest.json`
- Engine execution wrapper: `engines/opencode-sandboxed.sh`
- Hook behavior: `hooks/ringer_nudge.py`

## Verification points
- Successful run writes run state under the configured state directory.
- Score output is visible through dashboard views.
- Fail-fast checks and ordering are enforced by lint/verify code in `ringer.py`.

## Common failure modes
- Missing engine config in manifest (lint failure in `TaskSpec` checks).
- Check command exits false from `manifest` checks.
- Model routing fallback to unknown model key when registry entries are missing.
