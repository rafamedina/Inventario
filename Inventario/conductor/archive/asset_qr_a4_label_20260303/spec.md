# Specification: Asset QR Code Relocation and A4 Label Printing

## 1. Overview
This track involves relocating the QR code functionality from the Odoo Asset form view (header) to the printed A4 asset labels. The QR code will serve as a quick link to the asset's detailed form view in Odoo, accessible by authorized (logged-in) users.

## 2. Functional Requirements
- **QR Code Removal**: Remove the QR code display from the Asset form view header (where it is currently defined).
- **QR Code in Labels**: Update the A4 label report template to include a QR code for each asset.
- **QR Placement**: The QR code must be positioned approximately 2cm to the right of the asset's identification code (`identificador_final`) on the label.
- **QR Destination**: The QR code must encode the URL to the specific asset's standard Odoo form view.
- **Access Control**: Standard Odoo authentication and access rights apply. Scanning the QR will require the user to log in if they don't have an active session.

## 3. Technical Requirements
- **QWeb Template Update**: Modify the `report_asset_label_template` in `views/templates.xml` to include the `barcode` component with `type="QR"`.
- **Form View Modification**: Remove the `qr_code` field from the Asset form view header in `views/views.xml`.
- **URL Generation**: Ensure the QR code encodes a relative or absolute URL to the asset's backend form view.

## 4. Acceptance Criteria
- [ ] The Asset form view header no longer displays a QR code.
- [ ] The printed A4 labels feature a scanable QR code.
- [ ] The QR code on the label is placed roughly 2cm to the right of the asset code.
- [ ] Scanning the QR code successfully redirects the user to that asset's Odoo form view (requiring login if necessary).

## 5. Out of Scope
- Public access to asset information without Odoo credentials.
- Redesigning the entire label layout beyond the QR code addition.
- Mobile-specific "lite" product sheets.
