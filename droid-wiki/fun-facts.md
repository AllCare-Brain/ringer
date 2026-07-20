# Fun Facts
Purpose: This page documents unusual but important behaviors that affect day-to-day use.

- `dashboard/ringside.html` is intentionally compact and optimized for quick task switching.
- A dedicated `mock_worker.py` exists for deterministic engine behavior in tests.
- `hooks/ringer_nudge.py` deduplicates messages and writes nudge hints as JSON payloads with run/task context.
- Some models in `registry/model-capabilities` intentionally show mixed confidence and explicit “unknown” gaps to prevent over-assumption.
- HUD behavior is coupled to run-state paths and expects files to be present; `hud` docs explicitly instruct editing source assets, not built bundles.
