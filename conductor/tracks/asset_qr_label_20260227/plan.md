# Implementation Plan: Asset QR and Label Printing

## Phase 1: QR Code Generation Logic
- [ ] Task: Write failing test for QR code field.
    - [ ] Assert that a new field `qr_code` exists on `inventory.asset` and correctly encodes a link or the ID.
- [ ] Task: Implement QR code computation in `models/models.py`.
    - [ ] Add a computed binary field or a URL-based field for the QR code.
    - [ ] Use Odoo's native QR generation or a standard library.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: QR Code Generation Logic' (Protocol in workflow.md)

## Phase 2: Label Report & Paper Format
- [ ] Task: Write failing test for the Label Report definition.
    - [ ] Verify that a report named `action_report_asset_label` exists and is linked to the model.
- [ ] Task: Define Paper Format for small labels.
    - [ ] Create an XML record for `report.paperformat` (e.g., 50x30mm).
- [ ] Task: Create QWeb Template for the label.
    - [ ] Implement the layout in `views/templates.xml` containing only `identificador_final`.
- [ ] Task: Define the Report Action.
    - [ ] Link the template and paper format in a new `ir.actions.report` record.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Label Report & Paper Format' (Protocol in workflow.md)

## Phase 3: UI Integration
- [ ] Task: Write failing test for UI elements.
    - [ ] Assert that the QR code field and the print button are present in the form view architecture.
- [ ] Task: Update Asset Form View.
    - [ ] Add the QR code widget at the top of the form.
    - [ ] Add the "Imprimir ID" button below the QR code.
- [ ] Task: Implement "Preview First" logic (if not default Odoo behavior).
    - [ ] Ensure the QR code links to a URL that renders the report or a preview page.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration' (Protocol in workflow.md)