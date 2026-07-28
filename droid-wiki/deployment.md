# Deployment
Purpose: This page documents release and distribution workflows currently present in source.

## Release pipeline
`.github/workflows/release.yml` defines a matrix release for `macos-latest`, `ubuntu-latest`, and `windows-latest` and uses Tauri build tooling for `hud`.

## Release steps
1. Checkout repository.
2. Install Linux packages for GUI dependencies.
3. Install Rust toolchain.
4. Run Tauri build with platform-specific output naming.

## Not managed by this task
- Factory/Droid upload and wiki CI hooks are explicitly skipped per user request.
