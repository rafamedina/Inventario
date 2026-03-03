# Implementation Plan: Subcategory Migration Fix (subcategory_migration_fix_20260303)

## Phase 1: Enhance Subcategory Views
- [ ] **Task: Update Subcategory Tree View**
    - [ ] Add `categoria_id` field to `view_inventory_subcategory_tree` in `Inventario/views/views.xml`.
- [ ] **Task: Add Subcategory Search View**
    - [ ] Create `view_inventory_subcategory_search` for model `inventory.subcategory`.
    - [ ] Include search by "nombre", "codigo", and "categoria_id".
    - [ ] Add filters for "Active" and Group By "Category".
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Enhance Subcategory Views' (Protocol in workflow.md)**

## Phase 2: Automated Validation
- [ ] **Task: Write TDD Tests for Subcategory Linkage**
    - [ ] Create `Inventario/tests/test_subcategory_link.py`.
    - [ ] Test that a subcategory requires a category.
    - [ ] Test that creating a subcategory with a category ID correctly establishes the relationship.
- [ ] **Task: Verify View Definitions**
    - [ ] Ensure the XML views are valid and the field is included.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Automated Validation' (Protocol in workflow.md)**
