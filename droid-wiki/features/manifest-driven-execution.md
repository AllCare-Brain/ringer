# Manifest-Driven Execution
Purpose: This page explains how manifests are parsed, validated, and executed.

Active contributors: Jonathan Edwards

## Core behavior
- `ringer.py` defines manifest schema classes and enforces required checks.
- Validation includes task structure, model declarations, and check expectations.
- Execution builds task plans and tracks active runs until all rounds complete.

## Key abstractions
| Abstraction | File evidence |
|---|---|
| Manifest | `ringer.py` |
| TaskSpec | `ringer.py` |
| Round/task scheduler | `ringer.py` |
| Active run tracking | `ringer.py`, `tests/test_active_runs.py` |

## Entry points for modification
- Add new manifest constraints in `ringer.py` parser/validator.
- Extend expected output checks in checks modules and manifest templates.

## Skip notes
- No legacy alternate manifest runtime was found as a parallel control path; execution remains the main CLI plane.
