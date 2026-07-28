# Run Workflow
Purpose: This page documents the standard manifest execution pipeline from draft to completion.

Active contributors: Jonathan Edwards

## Typical workflow
1. Choose kit or custom manifest.
2. Lint manifest.
3. Run with desired concurrency/round settings.
4. Monitor via dashboard/HUD.
5. Inspect score and artifact outputs.

## Files used
- `ringer.py`
- `templates/` kits and checks
- `dashboard/` web surfaces
- `hud/` if local native monitoring is preferred

## Verification
- Confirm expected files exist and checks are not placeholders.
- Confirm score and identity pages render with expected metadata.
