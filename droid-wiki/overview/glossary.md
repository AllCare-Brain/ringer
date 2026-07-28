# Glossary
Purpose: This glossary defines terms used across manifest docs, dashboards, and run logs.

| Term | Meaning |
|---|---|
| Kit | Template family with `manifest.json`, `README.md`, and checks |
| Manifest | The task spec file for one run |
| Round | A named run stage; tasks are scheduled within rounds |
| Worker | Engine-backed unit that performs a task |
| Check | A validation command attached to a task or round |
| Score | Evaluated numeric/objective result generated from checks |
| Active run | Run currently tracked in memory plus persisted state files |
| Artifact | A final output file recorded in run artifact folders |
| Registry | `registry/*.toml` files mapping model names and capabilities |
| Nudge | Pre/Post tool hook output for guardrail or reminder behavior |
| HUD | Native Tauri status app under `hud/` |

## Cross references
- See manifest schema details in `droid-wiki/modules/manifest-schema.md`.
- See active run behavior in `droid-wiki/systems/execution-core.md`.
