# Engine Gateway Service
Purpose: This page explains how engine calls are normalized into a consistent worker abstraction.

Active contributors: Jonathan Edwards

## Scope
The gateway logic resides in core runner code and maps manifest-selected engines to:
- command invocation
- sandbox behavior
- provider metadata and response handling

## Relevant source
- `ringer.py`
- `engines/opencode-sandboxed.sh`
- `engines/mock_worker.py`
- `registry/model-identity.toml`

## Entry points
- Add new engine adapter in runner mapping blocks.
- Update sandbox behavior in engine-specific scripts.

## Risks
- Provider-specific parameter support varies per model and provider. Require explicit routing behavior checks for sensitive parameters.
