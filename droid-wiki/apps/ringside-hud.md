# Ringside HUD
Purpose: This page documents the native HUD app and how it consumes Ringer run-state.

Active contributors: Jonathan Edwards

## Purpose
`hud/` provides an always-on-top mission-control surface for live run visibility with tray integration.

## Key source files
| File | Role |
|---|---|
| `hud/src/main.rs` | Tauri command layer, tray/menu, polling, settings, artifact reads |
| `hud/frontend/hud.js` | Runtime state rendering and run list behavior |
| `hud/tauri.conf.json` | App packaging and permissions |
| `hud/Cargo.toml` | Native package metadata |

## Layout and behavior
- Polls state directory for active/finished runs.
- Supports hide/show tray controls.
- Reads artifact files and scoreboard structures for UI updates.

## Directory-layout table
| Path | Role |
|---|---|
| `hud/src` | Backend command handlers |
| `hud/frontend` | JS UI |
| `hud/scripts` | Build/runtime helpers |
| `hud/icons` | Platform assets |

## Modification points
- Add new HUD panels in `hud/frontend/hud.js`.
- Add new backend commands in `hud/src/main.rs`.
- Do not edit `dist/`; `hud/README.md` explicitly directs edits to source assets.
