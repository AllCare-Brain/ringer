# Kit Lifecycle
Purpose: This page captures how a kit moves from design to execution.

Active contributors: Jonathan Edwards

## Phases
- Design: create/choose kit manifest, role, boundary.
- Fill: resolve placeholders and check commands.
- Validate: `./ringer.py lint` and local smoke test.
- Execute: run manifests via chosen engine.
- Review: check findings and artifact outputs.

## Evidence source
- `templates/README.md`
- `templates/*/manifest.json`
- `templates/*/checks/*`

## Common gotchas
- Avoid leaving generic placeholders unresolved.
- Ensure `expect_files` is realistic and enforceable.
