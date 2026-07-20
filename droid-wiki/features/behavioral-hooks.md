# Behavioral Hooks
Purpose: This page describes hook behavior that nudges tool and run workflows.

Active contributors: Jonathan Edwards

## Hook scope
`hooks/ringer_nudge.py` implements pre/post tool nudges and deduping behavior.

## Notable behavior
- Parses tool event payload and emits bounded nudges.
- Deduplicates repeated messages.
- Adds run/task context when available.

## Integration points
- CLI / engine wrappers call into this hook behavior via hook configuration.
- Useful for agent behavior consistency and operational friction reduction.

## Skip reason
- No framework-level plugin bus exists outside this hook module; integration is explicit at call sites.
