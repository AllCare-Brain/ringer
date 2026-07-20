# Model Identity and Capabilities
Purpose: This page describes how model display names, access notes, and capabilities are resolved.

Active contributors: Jonathan Edwards

## Registry structure
- `registry/model-identity.toml` holds model-to-display mapping, defaults, and confidence.
- `registry/model-capabilities/*.toml` holds feature-by-feature behavior notes.

## Why this exists
The system separates model transport key from human-facing model taxonomy to avoid conflating engine and model names.

## Evidence files
- `registry/model-identity.toml`
- `registry/model-capabilities/glm-5.2.toml`
- `registry/model-capabilities/grok-build.toml`
- `registry/model-capabilities/gpt-5.5.toml`
- `registry/model-capabilities/openrouter-platform.toml`

## Update guidance
- Update registry files before changing any behavior that depends on provider/model feature differences.
- Preserve confidence states (`verified` vs `unverified`) until evidence updates exist.
