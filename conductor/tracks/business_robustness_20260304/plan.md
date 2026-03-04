# Implementation Plan: Business Robustness and Data Integrity

## Phase 1: Robustness Infrastructure (Tests First)
Create the failing tests that will define our robustness goals.

- [ ] Task: Create `test_business_robustness.py`
    - [ ] Write `test_prevent_category_deletion_with_assets`.
    - [ ] Write `test_prevent_location_deletion_with_assets`.
    - [ ] Write `test_enforce_unique_asset_id`.
    - [ ] Write `test_restrict_done_maintenance_deletion`.
- [ ] Task: Update `tests/__init__.py`
    - [ ] Add the new test file to the imports.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Robustness Infrastructure' (Protocol in workflow.md)

## Phase 2: Implementation of Logic
Apply the constraints to the models.

- [ ] Task: Update `InventoryCategory` and `InventoryLocation`
    - [ ] Override `unlink()` to check for related records and raise `UserError`.
- [ ] Task: Update `InventoryAsset` SQL Constraints
    - [ ] Add `_sql_constraints` for `identificador_final_unique`.
- [ ] Task: Secure Maintenance History
    - [ ] Override `unlink()` in `inventory.asset.maintenance` to block deletion if `state == 'done'`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Implementation of Logic' (Protocol in workflow.md)

## Phase 3: Verification
Ensure the suite is green.

- [ ] Task: Execute Suite and Verify
    - [ ] Run all tests and confirm 100% pass rate.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Verification' (Protocol in workflow.md)
