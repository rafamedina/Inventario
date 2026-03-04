# Implementation Plan: Global Integrity and Test Updates

## Phase 1: Security Fixes (Filters) [checkpoint: 37e1b24]
Address the identified information leakage in the UI.

- [x] Task: Restrict Search Filters 22d8354
    - [x] Edit `Inventario/views/views.xml` to add `groups="group_inventory_manager"` to the filters in `view_employee_filter_inherit_inventory`.
- [x] Task: Manual Verification - Search Filters
    - [x] Log in with a standard user and confirm the "Con Activos Asignados" filters are no longer visible in the Employees view.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Security Fixes (Filters)' (Protocol in workflow.md)

## Phase 2: Fix Obsolete Tests [checkpoint: 6a6e1a7]
Bring the test suite back to a green state.

- [x] Task: Refactor `test_asset_qr.py` e7a0360
    - [x] Update `test_ui_elements_in_view` to verify the QR code is NOT in the form view header (assert absent).
- [x] Task: Fix `test_subcategory_link.py` ba1bdd1
    - [x] Investigate and fix the `ForeignKeyViolation` during `sub.unlink()` in `test_migration_logic`. Likely need to unlink related plans first.
- [x] Task: Execute Suite and Verify 8ed555c
    - [x] Run all tests and confirm 100% pass rate for the module.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Fix Obsolete Tests' (Protocol in workflow.md)

## Phase 3: Final Audit and Cleanup
Ensure consistency across the module.

- [~] Task: Final XML Grep
    - [ ] Search for any other `hr.employee` inherited fields that might be missing group protection.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Audit and Cleanup' (Protocol in workflow.md)
