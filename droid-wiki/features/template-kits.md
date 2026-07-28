# Template Kits
Purpose: This page documents the reusable manifest kit system and its role in reducing task-specific drift.

Active contributors: Jonathan Edwards

## What kits provide
- A manifest skeleton (`manifest.json`).
- Optional check and prompt helpers.
- Reusable process boundary for review/fix/deploy workflows.

## Coverage
`templates/README.md` states the intended lifecycle: choose a kit, fill placeholders, then lint before run.

## Key evidence
| Kit category | Representative path |
|---|---|
| Multi-worker review | `templates/review-swarm/` |
| Fix patches | `templates/fix-swarm/` |
| Focused experiments | `templates/focus-group/` |
| Launch planning | `templates/launch-kit/` |
| Repo edits | `templates/repo-feature/` |
| Research proof | `templates/research-with-proof/` |

## Entry points
- Add new kit assets under `templates/<kit-name>/`.
- Add or update validation checks under `templates/<kit>/checks/`.

## Practical gotcha
- Keep checks executable and failing when they fail; empty `exit 0` stubs reduce safety.
