# Security
Purpose: This page summarizes security-relevant behavior and trust boundaries.

## Security posture
- No API secrets are committed; configuration is externalized.
- OpenCode execution can be sandboxed via wrapper and path allowlists.
- Model provider tokens/keys are loaded from runtime environment or local auth flows, not from repository files.

## Notable controls
- `engines/opencode-sandboxed.sh` uses filesystem restrictions and optional escape hatches for full access modes.
- Hooks and scripts preserve read-only mode where possible and append metadata rather than mutate source.
- HUD docs instruct editing sources, not bundled artifacts, reducing accidental tamper.

## Risks and mitigations
- Mixed-provider capabilities can cause unexpected parameter behavior; enforce `provider.require_parameters` when required.
- Model registry entries can drift; source files should be treated as evidence source and updated from verified references.
