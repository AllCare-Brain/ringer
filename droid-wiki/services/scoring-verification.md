# Scoring and Verification Service
Purpose: This page defines how check results become final run signals.

Active contributors: Jonathan Edwards

## Verification surfaces
- Check pass/fail and order enforcement.
- Score computation tied to worker and manifest-level expectations.
- Identity evidence and model-level annotations for observability.

## Key files
- `ringer.py` (verification and scoring codepaths)
- `tests/test_model_log.py`
- `tests/test_verify_order.py`
- `tests/test_lint.py`

## Entry points
- Tweak scoring/verification rules in `ringer.py`.
- Add tests that lock expected transitions.
