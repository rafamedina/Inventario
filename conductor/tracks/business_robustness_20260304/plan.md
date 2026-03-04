# Implementation Plan: Business Robustness and Data Integrity

## Phase 1: Robustness Infrastructure (Tests First) [checkpoint: Phase 1 Complete]
Create the failing tests that will define our robustness goals.

- [x] Task: Create `test_business_robustness.py`
    - [x] Write `test_prevent_category_deletion_with_assets`.
    - [x] Write `test_prevent_location_deletion_with_assets`.
    - [x] Write `test_enforce_unique_asset_id`.
    - [x] Write `test_restrict_done_maintenance_deletion`.
- [x] Task: Update `tests/__init__.py`
    - [x] Add the new test file to the imports.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Robustness Infrastructure' (Protocol in workflow.md)

## Phase 2: Implementation of Logic [checkpoint: b87a40c]
Apply the constraints to the models.

- [x] Task: Update `InventoryCategory` and `InventoryLocation` 7894a40
    - [x] Override `unlink()` to check for related records and raise `UserError`.
- [x] Task: Update `InventoryAsset` SQL Constraints 0eb33ef
    - [x] Add `_sql_constraints` for `identificador_final_unique`.
- [x] Task: Secure Maintenance History 235e33c
    - [x] Override `unlink()` in `inventory.asset.maintenance` to block deletion if `state == 'done'`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implementation of Logic' (Protocol in workflow.md)

## Phase 3: Verification
Ensure the suite is green.

- [~] Task: Execute Suite and Verify
    - [ ] Run all tests and confirm 100% pass rate.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Verification' (Protocol in workflow.md)
