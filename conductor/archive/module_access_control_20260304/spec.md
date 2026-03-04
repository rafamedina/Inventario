# Specification: Module Access Control for Inventario

## Overview
Implement module-level access control for the `Inventario` module. Access will be managed via a dedicated security group. Only users in this group will be able to see the module's root menu and perform operations.

## Functional Requirements
- **Security Group Creation**: Define a new security group named "Inventory / Full Access" (Internal ID: `group_inventory_manager`).
- **Access Rights**: Update `ir.model.access.csv` to grant full permissions (read, write, create, unlink) for all module models ONLY to the "Inventory / Full Access" group.
- **Menu Restriction**: Restrict the root menu `menu_inventory_root` so it is only visible to users in the "Inventory / Full Access" group.
- **Manual Assignment**: Access must be manually granted by an Odoo administrator to each user via the user settings.

## Non-Functional Requirements
- **Usability**: The administrator should easily find the group under the "Technical / Groups" or the user settings page.
- **Security**: Prevent unauthorized users from accessing the module via direct URLs or search.

## Acceptance Criteria
- [ ] A new group "Inventory / Full Access" appears in Odoo settings.
- [ ] A user without this group cannot see the "Gestión de Activos" menu in the Odoo home screen.
- [ ] A user with this group can see the module and perform all operations (CRUD) on assets, categories, subcategories, locations, and maintenance records.

## Out of Scope
- Granular permissions (e.g., a "Viewer" role with read-only access).
- Field-level security restrictions.
- Automation for auto-assigning the group to new users.
