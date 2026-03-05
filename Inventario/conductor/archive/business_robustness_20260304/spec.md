# Specification: Business Robustness and Data Integrity

## Overview
Transform the `Inventario` module into a robust, enterprise-grade application by implementing strict business constraints and data integrity rules. This track ensures that critical data cannot be accidentally deleted or duplicated.

## Functional Requirements
- **Deletion Protection**:
    - Prevent deleting an `inventory.category` if it has subcategories or assets.
    - Prevent deleting an `inventory.location` if it has assets.
    - Raise a `UserError` with a clear message in Spanish when a violation occurs.
- **Uniqueness Enforcement**:
    - Implement a `_sql_constraints` on `inventory.asset` to ensure `identificador_final` is unique across the entire database.
- **Maintenance History Lock**:
    - Restrict the deletion of `inventory.asset.maintenance` records that are in the 'done' state. Only users with "Access Rights" permissions (Settings > Users > Manage Users) should be able to override this (handled by default Odoo ACLs + custom Python check).

## Non-Functional Requirements
- **Security**: Hard integrity at the database level using SQL constraints where possible.
- **UX**: Professional error messages in Spanish that explain *why* the action was blocked.

## Acceptance Criteria
- [ ] Attempting to delete a category with assets results in a popup error: "No puedes eliminar esta categoría porque tiene activos asociados."
- [ ] Creating an asset with a duplicate ID results in a database integrity error.
- [ ] Non-admin users cannot delete completed maintenance records.
- [ ] All robustness tests pass.

## Out of Scope
- Changing the underlying data model (adding new fields).
- Automated data archiving.
- Field-level encryption.
