# 0001 — Native four-phase TRIP instead of adopting upstream TRIP

Date: 2026-07-14
Status: accepted

## Context

- Upstream TRIP (PiLastDigit/TRIP-workflow) v2 uses three phases: Plan, Implement, Release. Review and testing are folded into Implement.
- Upstream ships as agent skill files with ARCHI.md as persistent memory, and its Release phase performs commits, tags, and pushes itself.
- AllCare already has Open Engine (Linear lifecycle, approvals, receipts), Ringer (executable-check verification, model scoreboard), and AllCare-Brain (persistent memory).
- The AllCare loop-engineering contract requires an independent checker for subjective work and human gates on anything leaving the building.

## Decision

Build TRIP natively as a Ringer composition kit (`templates/trip-lifecycle`) instead of cloning or vendoring upstream TRIP.

- Keep Review as a standalone fourth phase with its own worker thread and, when available, a different scoreboard-selected model identity.
- Require a machine-readable Review verdict so Open Engine can route rounds deterministically.
- Release produces evidence only; all side effects stay pending and human-gated in Open Engine.
- No ARCHI.md: AllCare-Brain is the single memory layer.
- No upstream skill files: phase prompts live in the manifest spec template.

## Consequences

- The kit's contracts and tests assume four phases; folding Review into Implement later would be a breaking rewrite.
- Future readers comparing against upstream TRIP v2 will see a deliberate divergence, not drift.
- The one upstream idea deferred, not rejected: a second-model review of the Plan before human approval. Add as a plan-check ring only if plan quality becomes the bottleneck.
- `adversarial-review` may implement the Review phase internally, but its report must end in the TRIP verdict format.
