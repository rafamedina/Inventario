# Specification: Track Maintenance Changes in Asset Form

## Overview
Enable auditing and editing of archived maintenance records directly from the Asset form's "Maintenance History" tab, ensuring all changes to notes and images are captured in the Odoo chatter.

## Functional Requirements
- **Editable Maintenance History:** Allow users to edit the "Checklist Notes", "Checklist Images", and "General Notes" of maintenance records that are in the `done` state, directly from the Asset form's "Maintenance History" tab.
- **Chatter Integration:** All modifications to these fields must be reflected in the chatter of the corresponding `inventory.asset.maintenance` record.
- **Standard Field Tracking:** Use Odoo's standard `tracking=True` on the relevant fields (`notes` and `image` in maintenance lines, and any general notes field) to ensure changes are logged as standard message updates.
- **User Permissions:** Maintenance records in the `done` state should be editable by users in the `Inventario.group_inventory_manager` group.

## Non-Functional Requirements
- **Data Integrity:** Edits should only be allowed for specific, non-critical fields (notes and evidence images). The core structure (tasks, dates, plan) of a completed maintenance should remain locked.

## Acceptance Criteria
- [ ] Users can edit notes and images in the "Maintenance History" tab of an Asset.
- [ ] Changes made to these fields trigger a message in the chatter of the modified `inventory.asset.maintenance` record.
- [ ] The history log shows "Old Value" vs "New Value" for notes.
- [ ] Images updated are correctly reflected in the chatter (log entry indicating change).

## Out of Scope
- Changing the maintenance state back to "In Progress".
- Editing the original maintenance plan associated with the completed maintenance.
- Modifying dates or tasks once the maintenance is marked as `done`.
