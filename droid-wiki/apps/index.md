# Applications
Purpose: This lens groups app-level surfaces and explains their responsibilities.

## Apps in scope
| App | Path | Description |
|---|---|---|
| Ringside HUD | `hud/` | Native mission-control desktop application |
| Ring dashboard web | `dashboard/` | Browser-based execution view |

## Directory layout
| File/Dir | Role |
|---|---|
| `hud/src/` | Tauri core backend logic |
| `hud/frontend/` | Frontend JS and dashboard interactions |
| `dashboard/` | Shared HTML dashboard templates |

## Entry points
- `hud` app build via `cargo tauri build`.
- Dashboard files are served by the local dashboard endpoint in `ringer.py`.
