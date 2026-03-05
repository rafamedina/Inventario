# Specification: Subcategory Migration Fix (subcategory_migration_fix_20260303)

## Overview
Fix the subcategory migration issue where the category link is lost during export/import by making the `categoria_id` field visible in the tree view and exportable. This allows users to include the parent category in their data migrations via the standard Odoo interface.

## Functional Requirements
- **Update Tree View:** Add `categoria_id` (Categoría) field to `view_inventory_subcategory_tree`.
- **Add Search View:** Create `view_inventory_subcategory_search` to allow:
    - Filtering by Category.
    - Grouping by Category.
- **Improved Export/Import:** Ensure the field is easily selectable in the standard Odoo Export wizard.

## Acceptance Criteria
- [ ] The "Categoría" column is visible in the Subcategories list view.
- [ ] Users can select "Categoría" (and its ID/External ID) in the Odoo Export wizard.
- [ ] Users can filter/group subcategories by Category in the interface.
- [ ] A successful import of a subcategory with a category link can be performed.

## Out of Scope
- Modifications to Assets, Locations, or other models.
- Automated data migration scripts.
