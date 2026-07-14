# TRIP Lifecycle

A native Ringer composition kit for Open Engine implementation work. It adds no scheduler, queue, retry loop, or second source of truth. Open Engine owns lifecycle state and approvals; Ringer runs and verifies each phase round.

## Contract

- One OPE implementation issue maps to one stable `run_name` and one Ringside artifact history.
- Plan, Implement, Review, and Release are separate Ringer manifests sharing that `run_name`.
- Each manifest carries a top-level `trip` envelope with `issue`, `phase`, and immutable positive `plan_version` fields. Ringer tolerates this extension; the kit checker and Open Engine enforce it.
- The approved manifest is the executable Plan for that round. A material scope, permission, deliverable, or acceptance-check change creates the next plan version instead of mutating an approved file.
- Workers never commit, push, tag, publish, deploy, or open PRs. A Release ring prepares evidence; Open Engine performs approved side effects with checkpointed read-back.
- Review uses a separate worker thread and, when available, a different scoreboard-selected model identity from implementation.
- Runtime logs remain under `~/.ringer/runs`. Approved manifests, review reports, and release packages ship with the implementation branch and PR.

## Build a round

Copy `manifest.json`, fill every placeholder, and keep the same `run_name` for every round of the issue. Set `trip.phase` to exactly one of `plan`, `implement`, `review`, or `release`. Increment `trip.plan_version` only when the approved envelope materially changes.

Before execution, run both validators:

```bash
./ringer.py lint /absolute/path/to/filled-manifest.json
python3 templates/trip-lifecycle/checks/trip_contract.py \
  manifest --manifest /absolute/path/to/filled-manifest.json \
  --ringer /absolute/path/to/ringer.py \
  --expected-run-name ope-305-trip-protocol \
  --expected-issue OPE-305
```

The manifest's `check` is the plan-declared phase check. Open Engine runs the external Ringer lint and TRIP manifest validation before execution; do not embed either validator recursively inside the phase check.

## Phase outputs

### Plan

The Plan round produces the filled manifest for the next approved round. Open Engine presents the exact file for human approval before Implement begins. Planning workers return blockers as artifacts; they do not ask the human directly.

Deferred upgrade path: upstream TRIP has a second model review the Plan before work starts. Human Plan approval is the stronger gate today; if plan quality ever becomes the bottleneck, add a cheap plan-check ring before the approval hold.

### Implement

Compose with `repo-feature`, `fix-swarm`, `test-hardening`, or another existing kit. Preserve their ownership boundaries and executable checks. A failed Ringer task gets Ringer's one native retry; Open Engine owns additional review/fix rounds.

### Review

The review report must end with one machine-readable verdict and no trailing prose:

```markdown
# TRIP Review

## Summary
...

## Findings
...

## Verification
- Command: `<exact command>`
- Result: pass

## Verdict
Verdict: APPROVED
```

Allowed verdicts are `APPROVED`, `REQUEST_CHANGES`, and `NEEDS_REWORK`. Validate with:

```bash
python3 templates/trip-lifecycle/checks/trip_contract.py \
  review --report review.md
```

Open Engine maps those verdicts to the Release gate, another Implement round, or a return to Plan. It does not create new Linear statuses.

### Release

The Release ring writes `release.json`. It records proof and pending side effects; it performs none of them:

```json
{
  "ope_issue": "OPE-305",
  "run_name": "ope-305-trip-protocol",
  "plan_version": 1,
  "commit_message": "feat: add native TRIP protocol",
  "changed_files": ["path/to/file"],
  "verification": [
    {"command": "python3 tests/test_trip_lifecycle.py -v", "result": "pass"}
  ],
  "side_effects": [
    {"name": "commit", "status": "pending"},
    {"name": "push", "status": "pending"},
    {"name": "pr", "status": "pending"}
  ]
}
```

Side-effect names are stable lowercase slugs and unique checkpoint keys. Every status must remain `pending` until Open Engine receives Release approval and performs the action. Repositories may omit or add actions according to their existing release policy.

Run release validation in the issue's dedicated worktree. `changed_files` must equal the repo's entire tracked-and-untracked change set, so any unrelated dirty work fails the check by design. When an issue's deliverables span multiple repos, produce one release package per repo with the same `ope_issue` and `run_name`, each validated against its own repo with its own side-effect checkpoints.

Open Engine supplies the trusted repository path, OPE issue, stable run name, and one `--verify-command` argument per approved manifest check. The run name must equal the lowercased issue or start with it plus `-`. Every durable verification entry must contain exactly `"result": "pass"`. The checker rejects a package unless its changed files and command list exactly match those trusted inputs, then executes every trusted command in the repository.

```bash
python3 templates/trip-lifecycle/checks/trip_contract.py \
  release --package release.json \
  --repo /absolute/path/to/repo \
  --expected-run-name ope-305-trip-protocol \
  --expected-issue OPE-305 \
  --verify-command 'python3 tests/test_trip_lifecycle.py -v'
```

## Orchestrator responsibilities

Lifecycle state, approvals, round caps, verdict routing, side-effect checkpoints, the hotfix lane, and the promotion smoke gate are Open Engine duties, not this kit's. The enforcing procedure is section 13 (TRIP lifecycle) of `gbrain-allcare/skills/open-agent-engine/references/ringer-execution-lane.md`, the single source of truth for the lifecycle. Terms live in `CONTEXT.md`; the upstream-divergence decision lives in `docs/adr/0001-native-four-phase-trip.md`.
