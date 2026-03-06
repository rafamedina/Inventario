# Track: Fix visual misalignment in maintenance history

## Overview
After adding a `notes` field to the `inventory.asset.maintenance.line` model and including it in the asset's form, the maintenance history record view (when clicking on a record in the "Historial Mantenimientos" tab) exhibits visual misalignment. This is likely due to the `notes` field (a `fields.Text` field) being included in the checklist list view without proper formatting or space allocation.

## Functional Requirements
- Correct the layout of the checklist lines in the maintenance history and active maintenance views to ensure all columns are aligned.
- Ensure the `notes` field is readable and editable (where appropriate) without breaking the list's structure.
- (Optimization) Use a more suitable widget or layout (like a modal or a simpler text field) for notes if the current `fields.Text` in the list is too disruptive.

## Non-Functional Requirements
- Maintain a clean and professional UI in Odoo 18.
- Ensure responsiveness for different screen sizes.

## Acceptance Criteria
1. Open an asset with at least one completed maintenance record.
2. Go to the "Historial Mantenimientos" tab and click on a record.
3. Verify that the checklist list (with `name`, `is_done`, `image`, and `notes`) is perfectly aligned.
4. Verify the same for the "Mantenimiento ACTIVO" tab.

## Out of Scope
- Adding new logic to the maintenance workflow.
- Changing the maintenance plan configuration.
