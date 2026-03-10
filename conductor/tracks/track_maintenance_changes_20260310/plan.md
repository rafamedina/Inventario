# Implementation Plan: Track Maintenance Changes in Asset Form

## Phase 1: Research and TDD Setup
- [ ] Task: Audit `inventory.asset.maintenance` and `inventory.asset.maintenance.line` models to identify where to add `tracking=True`.
- [ ] Task: Identify the exact Odoo 18 view structure for the maintenance history list on the Asset form.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Research and TDD Setup' (Protocol in workflow.md)

## Phase 2: Backend Implementation - Field Tracking
- [ ] Task: Write a test case that creates a maintenance record in the 'done' state and verifies that changing notes/images does NOT log a message in the chatter yet.
- [ ] Task: Update the Python models to enable tracking on `notes` and `image` fields in `inventory.asset.maintenance.line`.
- [ ] Task: Ensure the parent `inventory.asset.maintenance` record is also configured to support chatter (inherit `mail.thread`).
- [ ] Task: Run tests and confirm that changes are now logged in the chatter.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Backend Implementation - Field Tracking' (Protocol in workflow.md)

## Phase 3: UI Implementation - Editable History
- [ ] Task: Update the XML view for the Asset form to make the maintenance history list editable even when the maintenance is 'done'.
- [ ] Task: Specifically ensure that `notes` and `image` fields are editable within the list view inside the Asset form.
- [ ] Task: Verify in the UI that an Inventory Manager can modify these fields from the "Maintenance History" tab.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Implementation - Editable History' (Protocol in workflow.md)

## Phase 4: Final Review and Checkpointing
- [ ] Task: Perform a final manual verification to confirm that changes to archived records are properly logged in the chatter.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Review and Checkpointing' (Protocol in workflow.md)
