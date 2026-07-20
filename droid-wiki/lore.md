# Lore
Purpose: This page records contextual history and non-obvious design choices to preserve team memory.

## Design rationale
- A single orchestrator (`ringer.py`) was retained as the control plane to keep manifest semantics consistent across multiple engines.
- The project uses explicit checks plus identity registry files rather than hardcoded provider mapping to avoid drift.
- The HUD is a separate native surface, not a mandatory dependency, so CLI-only operations remain lightweight.

## Notable operational conventions
- Templates are expected to be assembled and then linted before running (`./ringer.py lint`).
- Check outputs are expected to produce meaningful failure details and are not treated as optional placeholders.
- Run state is the interoperability contract for dashboards and Tauri polling.

## Recorded assumptions that influence implementation
- Engine names and model names are treated differently; model display taxonomy is resolved from `registry/model-identity.toml`.
- For long-context tooling behavior, malformed tool JSON is treated as recoverable where relevant with parse validation and retries.

## References
- `README.md`
- `docs/STEERING.md`
- `registry/model-identity.toml`
