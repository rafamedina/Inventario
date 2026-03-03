# Implementation Plan: Asset QR Code Relocation and Label Printing

## Phase 1: Preparation and Environment Setup
- [x] Task: Review existing label report and form view definitions in `views/views.xml` and `views/templates.xml`. 
- [x] Task: Identify the exact URL structure needed for the QR code to link to the asset form view. 

## Phase 2: QR Code Removal from Form View (TDD) [checkpoint: 5d35462]
- [x] Task: Write failing test: Verify that the asset form view does NOT contain the `qr_code` element in the header. 1acc300
- [x] Task: Implement change: Remove the `qr_code` field definition from the Asset form view header in `views/views.xml`. 1acc300
- [x] Task: Verify tests pass. 1acc300
- [x] Task: Conductor - User Manual Verification 'Phase 2: QR Code Removal from Form View' (Protocol in workflow.md) 5d35462

## Phase 3: QR Code Integration into Printed Label (TDD)
- [x] Task: Write failing test: Verify that the A4 label report template includes a barcode component of type 'QR'. 
- [ ] Task: Implement change: Update the `report_asset_label_template` QWeb template to include the QR code.
- [ ] Task: Style change: Position the QR code approximately 2cm to the right of the asset ID/code using inline CSS or a style block.
- [ ] Task: Implement URL logic: Ensure the QR code encodes the Odoo form view URL for the specific asset.
- [ ] Task: Verify tests pass and check the generated PDF report output.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: QR Code Integration into Printed Label' (Protocol in workflow.md)

## Phase 4: Final Verification and Cleanup
- [ ] Task: End-to-end manual test: Print a label, scan the QR code, and verify it opens the correct asset record after login.
- [ ] Task: Ensure overall code coverage for the `Inventario` module remains >80%.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Verification and Cleanup' (Protocol in workflow.md)
