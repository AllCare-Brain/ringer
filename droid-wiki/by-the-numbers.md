# By the Numbers
Purpose: This page captures concrete repository-size and behavior evidence for planning and onboarding.

## Repository footprint (source of truth)
- `ringer.py` length: `9131` lines.
- Template kits: `15` (`templates/*/manifest.json` count).
- Number of kit families: `15` directories under `templates/`.
- Test files in `tests/`: `26`.
- Engine wrappers in `engines/`: `2`.
- HUD files in `hud/`: `62` tracked files.

## Files by domain
| Area | Count proxy |
|---|---:|
| Templates | 15 kits |
| Checks folders | many, within each kit |
| Tests | 26 files |
| Docs | several markdown + images |
| CI workflows | 1 release workflow |

## Operational signals
- Core command surface includes run, lint, hud, db/models/catalog/debug-style commands in `ringer.py`.
- Runbooks are manifest-driven and can be expanded via new kits/checks without changing core behavior.
