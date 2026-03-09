# Specification: Professional Odoo CI/CD Standard

## Overview
Full migration to the Professional Odoo DevOps standard based on proven industry patterns. This architecture replaces generic test runners with Odoo's native testing engine and implements advanced observability.

## Architectural Changes

### 1. Docker Multi-stage Optimization
- **Test Stage**: Now includes Google Chrome Stable and `chromium-browser` wrapper. This enables **JS Tours** and UI testing within the CI.
- **Production Stage**: Implements a "Zero-Waste" policy, stripping all development metadata, tests, and CI configurations from the final image.

### 2. Testing Engine: Odoo Native
- **Mechanism**: Switched from `pytest-odoo` to `odoo --test-enable`.
- **Automatic DB Provisioning**: Odoo now creates, initializes, and destroys the test databases (`test_ci_db_unit` and `test_ci_db_int`) automatically. This eliminates "Database not found" and "Connection refused" errors.
- **Isolation**: Unit and Integration tests run in separate, ephemeral databases to ensure zero cross-test contamination.

### 3. CI/CD Performance & Artifacts
- **Image Compression**: Images are now `gzip` compressed before being uploaded as artifacts. This reduces network overhead and speeds up the transition between the `build` job and `test` jobs.
- **Atomic Builds**: The module is built exactly once. The same compressed binary is then used for all subsequent testing stages.

### 4. Advanced Observability (Log Analysis)
- **Log Parsing**: Implemented a sophisticated bash parser that:
    - Extracts precise failure/error counts.
    - Captures detailed Python Tracebacks.
    - Specifically monitors for **JS Tour failures**.
    - Fails the build on any `ERROR` or `CRITICAL` log entry, even if the process exit code is 0.

## Implementation Details
- **Module Name**: `Inventario`
- **Environment**: GitHub Actions + PostgreSQL 15 Service Containers.
- **Triggers**: Push/PR to `18.0-dev`, `master`, and manual `workflow_dispatch`.
