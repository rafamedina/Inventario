# Specification: Employee History Code Display (employee_history_id_20260303)

## Overview
Update the "Historial de Asignaciones" tab in the employee form to display the asset's standardized ID instead of its name. This ensures that IT administrators can identify specific physical assets directly from the employee's history.

## Functional Requirements
- **Update Employee View:** Modify the embedded tree view within `view_employee_form_inventory_simple`.
- **Change Column Display:** Within the `asset_history_ids` field, replace the default asset display with the `identificador_final` field from the linked asset.
- **Maintain Traceability:** Ensure the relationship between the history record and the asset record remains intact.

## Acceptance Criteria
- [ ] In the Employee form (Inventory view), the "Historial de Asignaciones" tab displays the "ID Estandarizado" of the assets.
- [ ] The asset's name is no longer displayed in this specific table.
- [ ] Clicking the ID in the table still opens the corresponding asset record.

## Out of Scope
- Modifications to the "Actual" assignment tables (Responsibilities/Property).
- Data migrations or model logic changes.
