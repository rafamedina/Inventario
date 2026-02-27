# Implementation Plan: Audit all functionality

## Phase 1: Environment and Baseline Verification
- [ ] Task: Verify current test suite status.
    - [ ] Run `test_id_generation.py`.
    - [ ] Run `test_import.py`.
    - [ ] Run `test_subcategory_link.py`.
- [ ] Task: Audit Odoo configuration files.
    - [ ] Verify `__manifest__.py` data loading.
    - [ ] Verify `ir.model.access.csv` permissions.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment and Baseline Verification' (Protocol in workflow.md)

## Phase 2: Functional Audit and Refinement
- [ ] Task: Test asset creation and ID generation.
    - [ ] Manually create an asset and check `identificador_final`.
- [ ] Task: Test maintenance lifecycle.
    - [ ] Set an asset's next maintenance date to today.
    - [ ] Run `check_maintenance_dates` method manually in shell.
    - [ ] Verify `mail.activity` is created.
    - [ ] Use `action_maintenance_done` and check next date calculation.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Functional Audit and Refinement' (Protocol in workflow.md)

## Phase 3: Final Verification
- [ ] Task: Run all tests one last time and ensure coverage.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Verification' (Protocol in workflow.md)
