# API Endpoints
Purpose: This page lists known dashboard and HUD-facing endpoints exposed by Ringer.

## Endpoint classes
- Active run endpoints for current statuses.
- Artifact and score endpoints for finished tasks.
- Log endpoints for troubleshooting.

## Primary references
- `ringer.py`.
- `tests/test_hud_server.py`.
- `tests/test_log_endpoint.py`.
- `dashboard/dashboard.html` and `dashboard/ringside.html`.

## Behavior expectation
- Endpoints must remain parseable by HUD and browser pages.
- Tests enforce expected payload shape for core dashboard paths.
