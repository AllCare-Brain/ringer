# Architecture
Purpose: This page documents how the repository components exchange data and control.

Ringer combines a Python CLI core with a native HUD and optional web dashboards. The design is intentionally event-oriented around a run state directory.

## Runtime topology
```mermaid
flowchart LR
A[Manifest file] --> B[CLI parser in ringer.py]
B --> C[Manifest validation and lint]
C --> D[Engine adapter (codex/grok/opencode)]
D --> E[Worker process/CLI/tooling]
E --> F[Task logs + run-state JSON]
F --> G[Scoring + verify checks]
G --> H[Artifact library]
F --> I[HTTP dashboard endpoints]
I --> J[dashboard HTML]
I --> K[Ringside HUD desktop app]
H --> L[artifact/exports and scoreboard]
```

## Major subsystems
- `Manifest` layer in `ringer.py` validates model/runtime, checks, and output expectations.
- Engine dispatch in `ringer.py` routes to codex/grok/opencode and reads `registry/` for display identity.
- Verification layer validates checker order, expected files, and score output.
- Artifacts service records JSON artifacts (`scores.json`, `identity.json`, etc.) and feed pages.
- HUD integration polls run state for live visibility and exposes tray controls.

## Data flow
1. User runs a manifest with `ringer.py run`.
2. Workers spawn according to rounds/task groups.
3. Each worker writes logs, artifacts, and task metadata.
4. Main orchestration verifies each check and updates active run state.
5. Scoring data is materialized for dashboards and final artifact pages.

## Integration points
- `registry/model-identity.toml` maps model slugs into display taxonomy.
- `registry/model-capabilities/*.toml` stores provider and behavior notes used for capability-aware routing.
- `templates/*/` defines reusable patterns that constrain manifests and checks.

## External dependencies
- External engines via their CLIs/APIs (Codex, Grok, OpenCode).
- Tauri toolchain for desktop HUD packaging in `hud/`.
- GitHub Actions for release matrix when publishing `ringside`.
