# TRIP Lifecycle — Glossary

Ubiquitous language for the Open Engine + Ringer + TRIP harness. Terms only; no implementation details.

## TRIP (native)

- AllCare's four-phase issue lifecycle: Plan, Implement, Review, Release.
- A deliberate adaptation of PiLastDigit's TRIP workflow.
- Diverges from upstream TRIP v2, which folded Review into Implement. Do not "upgrade" to three phases.

## Phase

- Exactly one of: `plan`, `implement`, `review`, `release`.
- Each phase runs as its own Ringer manifest.

## Round

- One executed Ringer run of one phase for one issue.
- An issue may take several Implement and Review rounds before Release.

## Ring

- The worker task(s) inside one round's manifest.

## run_name

- The stable identifier binding every round of one OPE issue to one Ringside artifact history.
- Must be the lowercased issue key, or start with it plus `-`.

## plan_version

- Immutable positive integer on an approved manifest.
- A material change to scope, permissions, deliverables, or acceptance checks creates the next plan version; it never mutates an approved file.

## Verdict

- The single machine-readable outcome of a Review round: `APPROVED`, `REQUEST_CHANGES`, or `NEEDS_REWORK`.
- The final non-empty line of the review report.

## Release package

- `release.json`: evidence of what was built and verified, plus pending side effects.
- Records side effects; performs none of them.

## Side effect

- An outward action (commit, push, pr, publish, deploy) that only Open Engine performs, after human Release approval.
- Stays `pending` in the Release package until then.

## Open Engine

- The Linear-based lifecycle owner: issue state, approvals, round caps, and side effects.

## Ringer

- The swarm executor: runs one round's manifest, executes checks, retries once, records evidence.

## Kit

- A reusable Ringer starter under `templates/`. Work kits (e.g. `repo-feature`) define worker jobs; `trip-lifecycle` is the issue envelope that composes them.
