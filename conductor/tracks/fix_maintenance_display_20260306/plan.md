# Implementation Plan - Fix maintenance display

## Phase 1: Research & Reproduction
- [ ] Task: Research Odoo 18 Many2one domain reactivity and verify why `plan_id` dropdown is empty.
- [ ] Task: Create `tests/` directory and `tests/__init__.py`.
- [ ] Task: Implement a failing test case in `tests/test_maintenance_plans.py` to reproduce the empty dropdown issue.
- [ ] Task: Conductor - User Manual Verification 'Research & Reproduction' (Protocol in workflow.md)

## Phase 2: Bug Fix Implementation
- [ ] Task: Update the `plan_id` field domain in `models/models.py` to be more robust.
- [ ] Task: Update `views/views.xml` to explicitly define the domain for `plan_id` for UI reactivity.
- [ ] Task: Verify the fix by running the test case and ensuring it passes.
- [ ] Task: Conductor - User Manual Verification 'Bug Fix Implementation' (Protocol in workflow.md)

## Phase 3: Finalization & Coverage
- [ ] Task: Run all tests and verify code coverage is above 90% for the changes.
- [ ] Task: Conductor - User Manual Verification 'Finalization & Coverage' (Protocol in workflow.md)
