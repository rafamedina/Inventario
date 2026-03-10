# Comprehensive Guide: CI/CD System for Odoo 18

This document consolidates all the information needed to understand, manage, and maintain the Continuous Integration and Deployment (CI/CD) pipeline for the Inventory module.

---

## 1. Explanation: Architecture and Logic
This section explains the concepts and logic behind the system.

### Purpose
The primary goal of this pipeline is to act as a **quality gatekeeper**. It ensures that the code in the production branch (`18.0-pre-prod`) is stable, secure, and free from unnecessary files that only make sense during development.

### The Workflow
The system uses a linear 5-stage flow designed to fail fast:
1.  **Style Validation:** Verifies that the code is readable and follows Python standards.
2.  **Unified Build:** Creates a single Docker image for all tests.
3.  **Isolation Testing (Unit):** Verifies the internal logic of the models.
4.  **Flow Testing (Integration):** Simulates end-user behavior using Chrome.
5.  **Promotion and Cleanup:** "Distills" the code for the production branch.

### "Clean Promotion" Logic
It implements **surgical cleaning**. Test files, AI configurations (`conductor/`), and GitHub workflows are removed so that the `18.0-pre-prod` branch is a pure version of the module, ready for the end client.

### Security Model
Operates under the **"Zero Trust"** principle: no default passwords are assumed, and all communication depends on secrets dynamically injected by GitHub.

---

## 2. How-to Guides
Step-by-step instructions for common tasks.

### How to configure the Postgres secret
1.  Navigate to your repository on GitHub > **Settings**.
2.  Go to **Secrets and variables** > **Actions**.
3.  Click **New repository secret**.
4.  **Name:** `POSTGRES_PASSWORD`.
5.  **Secret:** Your password (e.g., `peter123`).

### How to trigger a build manually
1.  Go to the **Actions** tab on GitHub.
2.  Select **Odoo Module CI/CD Professional**.
3.  Click **Run workflow**.

### How to read test results
1.  Enter the failed execution and open the **Unit Tests** or **Integration Tests** Job.
2.  Look for the **Analyze Test Results** step.
3.  You will see the test summary and critical error count.

### How to download full logs
1.  In the execution "Summary", look for the **Artifacts** section.
2.  Download `unit-test-logs` or `integration-test-logs`.

---

## 3. Technical Reference
Technical details, variables, and limits.

### Environment Variables
| Variable | Purpose | Default Value |
| :--- | :--- | :--- |
| `ODOO_DB` | Base database name | `test_ci_db` |
| `POSTGRES_USER` | Database user | `odoo` |
| `POSTGRES_PASSWORD` | Password (via Secret) | (No fallback) |
| `DOCKER_IMAGE` | Image name | `odoo-inventario-test` |

### Jobs and Timeouts
| Job | Max Time | Description |
| :--- | :--- | :--- |
| `lint` | 5 min | Static analysis with Ruff. |
| `build` | 15 min | Docker build with GHA cache. |
| `test-unit` | 15 min | Odoo tests (excluding `-ui`). |
| `test-integration`| 20 min | Odoo tours with Chrome Headless. |
| `promote` | 10 min | Cleanup and Push to Pre-Prod. |

### Artifacts and Tags
*   **Retention:** 1 day for images, 7 days for logs.
*   **Tags:** `v18.0-build-${{ github.run_number }}`.
