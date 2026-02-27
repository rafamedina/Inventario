# Implementation Plan: Asset QR and Label Printing

## Phase 1: QR Code Generation Logic [checkpoint: b46c524]
- [x] Task: Write failing test for QR code field. c7f9455
    - [x] Assert that a new field `qr_code` exists on `inventory.asset` and correctly encodes a link or the ID.
- [x] Task: Implement QR code computation in `models/models.py`. c7f9455
    - [x] Add a computed binary field or a URL-based field for the QR code.
    - [x] Use Odoo's native QR generation or a standard library.
- [x] Task: Conductor - User Manual Verification 'Phase 1: QR Code Generation Logic' (Protocol in workflow.md)

## Phase 2: Label Report & Paper Format [checkpoint: 6b292a4]
- [x] Task: Write failing test for the Label Report definition. 348a992
    - [x] Verify that a report named `action_report_asset_label` exists and is linked to the model.
- [x] Task: Define Paper Format for small labels. 6b292a4
    - [x] Create an XML record for `report.paperformat` (e.g., 50x30mm).
- [x] Task: Create QWeb Template for the label. 6b292a4
    - [x] Implement the layout in `views/templates.xml` containing only `identificador_final`.
- [x] Task: Define the Report Action. 6b292a4
    - [x] Link the template and paper format in a new `ir.actions.report` record.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Label Report & Paper Format' (Protocol in workflow.md)

## Phase 3: UI Integration
- [~] Task: Write failing test for UI elements.
    - [ ] Assert that the QR code field and the print button are present in the form view architecture.
- [ ] Task: Update Asset Form View.
    - [ ] Add the QR code widget at the top of the form.
    - [ ] Add the "Imprimir ID" button below the QR code.
- [ ] Task: Implement "Preview First" logic (if not default Odoo behavior).
    - [ ] Ensure the QR code links to a URL that renders the report or a preview page.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration' (Protocol in workflow.md)