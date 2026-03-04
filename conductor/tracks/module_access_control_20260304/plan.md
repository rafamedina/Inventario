# Implementation Plan: Module Access Control for Inventario

## Phase 1: Define Security Group
Create the foundational security group for managing access to the module.

- [x] Task: Create security XML file 87f5f4a
    - [x] Create `Inventario/security/security_groups.xml` defining `group_inventory_manager` as "Inventory / Full Access".
- [x] Task: Update Manifest 2304173
    - [x] Add `security/security_groups.xml` to the `data` list in `Inventario/__manifest__.py` (it MUST be loaded before `ir.model.access.csv`).
- [x] Task: TDD - Verify Group Creation a6cc589
    - [x] Write a test case in a new test file `Inventario/tests/test_security_groups.py` to ensure the group is correctly created in the database.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Define Security Group' (Protocol in workflow.md)

## Phase 2: Apply Access Rights
Restrict CRUD operations on models to the new security group.

- [ ] Task: TDD - Verify Restricted Access (Failure)
    - [ ] Write a test in `Inventario/tests/test_security_groups.py` where a standard internal user (without the new group) tries to read or create an asset. Confirm it fails as expected.
- [ ] Task: Update `ir.model.access.csv`
    - [ ] Replace `base.group_user` with `Inventario.group_inventory_manager` for all models in the CSV file.
- [ ] Task: TDD - Verify Granted Access (Success)
    - [ ] Write a test where a user WITH the new group tries to perform CRUD operations on an asset. Confirm it succeeds.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Apply Access Rights' (Protocol in workflow.md)

## Phase 3: Menu Restriction
Hide the module's root menu for unauthorized users.

- [ ] Task: Update Menu Visibility
    - [ ] Edit `Inventario/views/views.xml` to add `groups="group_inventory_manager"` to the `menu_inventory_root` menuitem.
- [ ] Task: TDD - Verify Menu Visibility
    - [ ] Write a test to check if the root menu is returned in the menu tree for a user in the group and not for a standard user.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Menu Restriction' (Protocol in workflow.md)

## Phase 4: Final Verification and Cleanup
Perform end-to-end checks and ensure consistency.

- [ ] Task: Full Test Suite Execution
    - [ ] Run all module tests to ensure no regressions.
- [ ] Task: Documentation Update
    - [ ] (Optional) Add a brief note in a README or similar file about how to grant access.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Verification and Cleanup' (Protocol in workflow.md)
