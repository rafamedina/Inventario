# Implementation Plan: Global Integrity and Test Updates

## Phase 1: Security Fixes (Filters)
Address the identified information leakage in the UI.

- [ ] Task: Restrict Search Filters
    - [ ] Edit `Inventario/views/views.xml` to add `groups="group_inventory_manager"` to the filters in `view_employee_filter_inherit_inventory`.
- [ ] Task: Manual Verification - Search Filters
    - [ ] Log in with a standard user and confirm the "Con Activos Asignados" filters are no longer visible in the Employees view.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Security Fixes (Filters)' (Protocol in workflow.md)

## Phase 2: Fix Obsolete Tests
Bring the test suite back to a green state.

- [ ] Task: Refactor `test_asset_qr.py`
    - [ ] Update `test_ui_elements_in_view` to verify the QR code is NOT in the form view header (assert absent).
    - [ ] (Optional) Add a check to verify the QR logic still works for the report template.
- [ ] Task: Fix `test_subcategory_link.py`
    - [ ] Investigate and fix the `ForeignKeyViolation` during `sub.unlink()` in `test_migration_logic`. Likely need to unlink related plans first.
- [ ] Task: Execute Suite and Verify
    - [ ] Run all tests and confirm 100% pass rate for the module.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Fix Obsolete Tests' (Protocol in workflow.md)

## Phase 3: Final Audit and Cleanup
Ensure consistency across the module.

- [ ] Task: Final XML Grep
    - [ ] Search for any other `hr.employee` inherited fields that might be missing group protection.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Audit and Cleanup' (Protocol in workflow.md)
