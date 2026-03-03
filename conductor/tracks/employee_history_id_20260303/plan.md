# Implementation Plan: Employee History Code Display (employee_history_id_20260303)

## Phase 1: Update UI
- [ ] **Task: Modify Employee Form View**
    - [ ] Locate `view_employee_form_inventory_simple` in `Inventario/views/views.xml`.
    - [ ] Find the tree view for `asset_history_ids`.
    - [ ] Replace `<field name="asset_id"/>` with `<field name="asset_id" string="Activo (ID)"/>`.
    - [ ] Check if `identificador_final` can be directly referenced as `asset_id.identificador_final`. If not, we will add a related field to the history model.
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Update UI' (Protocol in workflow.md)**

## Phase 2: Verification
- [ ] **Task: Visual Check**
    - [ ] Verify that the column header and content now reflect the Standardized ID.
    - [ ] Verify that the name is hidden.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Verification' (Protocol in workflow.md)**
