# Configuration Module
Purpose: This page documents local configuration sources and their operational impact.

Active contributors: Jonathan Edwards

## Config surfaces
- `config.sample.toml` for documented defaults.
- Runtime state path defaults from environment and config.

## Practical effect
- HUD and dashboard polling use configured paths under user config.
- Engine auth and run behavior can be influenced by local config and environment.

## Key references
- `config.sample.toml`
- `ringer.py`
- `hud/README.md`

## Notes
- `config.sample.toml` is intentionally a template, not a live secrets file.
