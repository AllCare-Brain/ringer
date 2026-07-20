# Artifacts and Scoreboard
Purpose: This page explains how scores, evidence, and final outputs are produced.

Active contributors: Jonathan Edwards

## Artifact flow
- Workers and checks produce logs and outputs.
- Scoring logic aggregates verification and check results.
- Scoreboard data and identity metadata are rendered in dashboards and artifacts.

## Relevant source files
| File | Role |
|---|---|
| `ringer.py` | Artifact and verification orchestration |
| `dashboard/dashboard.html` | Web scoreboard view |
| `dashboard/ringside.html` | Compact runtime and scoring UI |

## Entry points for extension
- Extend artifact schema in `ringer.py` verification and rendering helpers.
- Add new artifact types with matching dashboard consumers.
