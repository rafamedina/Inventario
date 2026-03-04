# Specification: Global Integrity and Test Updates

## Overview
Perform a global cleanup and integrity check of the `Inventario` module. This includes fixing information leakage in search filters, updating obsolete tests from previous tracks (QR relocation and subcategory logic), and ensuring security group consistency.

## Functional Requirements
- **Search Filter Restriction**: Add `groups="Inventario.group_inventory_manager"` to the custom search filters in `view_employee_filter_inherit_inventory` to prevent unauthorized users from identifying which employees have assets.
- **Legacy Test Refactoring**:
    - `test_asset_qr`: Update tests to reflect that the QR code is no longer in the form view header but in the printed labels.
    - `test_subcategory_link`: Fix the `unlink` foreign key violation error in the migration test logic.
- **Security Audit**: Verify that no other UI elements or menus are leaking information to users outside the `group_inventory_manager`.

## Non-Functional Requirements
- **Maintainability**: Ensure the test suite is green and reliable for future developments.
- **Privacy**: Adhere to the principle of least privilege by hiding identifying filters from non-module users.

## Acceptance Criteria
- [ ] All tests in the `Inventario` module pass when running with `--test-enable`.
- [ ] Users without the "Inventory / Full Access" group cannot see asset-related filters in the Employees search view.
- [ ] Security group configuration remains strictly separated from Odoo base groups (No implied inheritance).

## Out of Scope
- Adding new functional features.
- Major refactoring of Odoo core models.
- Changing the QR code destination URL.
