# Engine Integrations
Purpose: This page captures how Ringer routes work between codex, grok, and opencode runtimes.

Active contributors: Jonathan Edwards

## Supported engines
- `codex` (Codex CLI based flow)
- `grok` (Grok Build CLI flow)
- `opencode` (OpenCode flow via provider API)

## Evidence-backed flow
- Engine names and manifests in `ringer.py`.
- Registry identity mapping in `registry/model-identity.toml`.
- Capability notes in `registry/model-capabilities/*.toml`.

## Behavioral notes
- Display identity is separated from model slugs to avoid mislabeling.
- OpenRouter/OpenCode behavior contains provider-specific limitations; `require_parameters` is relevant when strict behavior is required.
- Mock worker exists for deterministic test execution (`engines/mock_worker.py`).

## Key files
| File | Purpose |
|---|---|
| `engines/opencode-sandboxed.sh` | OpenCode sandbox wrapper |
| `engines/mock_worker.py` | Deterministic mock engine responses |
| `registry/model-identity.toml` | Model display and access metadata |
