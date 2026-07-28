# Contributing to Ringer
Purpose: This page gives contribution expectations for code, templates, and infra changes.

## Start here
- Read `README.md` for baseline project intent.
- Keep PRs scoped to one behavior per change.
- Add/adjust tests for orchestration logic and script output behavior in `tests/`.

## Source map for contributors
- Core logic edits are mainly in `ringer.py`.
- Template work is in `templates/`.
- Dashboard/HUD behavior lives in `dashboard/` and `hud/`.
- Shell and Python helpers are in `engines/`, `hooks/`, `scripts/`.

## Safety guardrails
- Do not write fake checks that always succeed.
- Preserve run-state schema compatibility where dashboards consume fields.
- Avoid adding secret values or sensitive logs to wiki/source docs.
