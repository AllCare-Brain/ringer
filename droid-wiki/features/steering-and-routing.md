# Steering and Routing
Purpose: This page explains steering policy, status transitions, and routing constraints.

Active contributors: Jonathan Edwards

## Steering profile
`docs/STEERING.md` documents route-level steering and rule semantics. `ringer.py` contains policy fields to express desired behavior and status outcomes.

## Runtime behavior
- Steering profile can affect how tasks are prioritized and how verification interprets outcomes.
- Steering status transitions are part of manifest semantics and check orchestration.
- Rules include hard exclusions, fallback semantics, and reason tracking.

## Entry points
- `docs/STEERING.md`
- `ringer.py` steering dataclasses and parsing logic
- `tests/test_steering.py`

## Skip reason for thin wrappers
- The steering implementation is embedded in the core execution path, so no separate steering service exists.
