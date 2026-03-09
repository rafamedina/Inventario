# Specification: CI/CD Pipeline Optimization & Security Hardening

## Overview
Refinement of the `Odoo Module CI/CD Professional` workflow to meet senior DevOps standards. The goal is to minimize the attack surface through restricted permissions, improve execution speed via caching, and increase the robustness of the production synchronization process.

## Key Improvements

### 1. Security: Least Privilege
- **Previous state**: Global `permissions: contents: write`.
- **New state**: Global `permissions: contents: read`. Specific `write` access is granted only to the `promote-to-preprod` job. This prevents accidental or malicious writes from other jobs.

### 2. Performance: Dependency Caching
- **Optimization**: Added `cache: "pip"` to the `actions/setup-python` step.
- **Impact**: Reduces setup time for the `lint` job by avoiding full re-installation of `ruff` on every run.

### 3. Operability: Manual Triggers
- **New trigger**: `workflow_dispatch`.
- **Benefit**: Allows developers to trigger the pipeline manually from the GitHub UI for testing or one-off builds without requiring a code commit.

### 4. Reliability: Job Guardrails
- **Timeouts**: Added `timeout-minutes` to every job to prevent stalled runners from consuming credits or blocking the queue.
- **Systematic Cleanup**: Refined the `promote-to-preprod` script to be more exhaustive in removing non-production files, ensuring the `18.0-pre-prod` branch remains lean and secure.

## Technical Architecture
- **Environment**: GitHub-hosted `ubuntu-latest`.
- **Services**: PostgreSQL 15 as a service container for unit and integration tests.
- **Docker**: Buildx with `gha` caching for efficient image builds.
- **Artifacts**: Inter-job communication via image export/import to ensure the exact same build is tested across stages.
