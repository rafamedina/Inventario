# Specification: Asset QR and Label Printing

## Overview
Implement a QR code generation and label printing feature for inventory assets. This allows users to quickly generate a physical label containing the asset's standardized ID by scanning a code or clicking a button directly from the Odoo form.

## Functional Requirements
- **QR Code Display:**
  - Generate a unique QR code for each `inventory.asset`.
  - Display the QR code prominently at the **Top of the Form** (near the name/ID).
- **Label Preview & Printing:**
  - Scanning the QR code leads to a **Preview First** page showing the label.
  - Add a mini button labeled **"Imprimir ID"** directly below the QR code.
  - Both the QR scan (preview) and the button should facilitate printing a **Small Label PDF**.
- **Label Content:**
  - The printed label must contain only the `identificador_final` of the asset.
  - The format must be optimized for small label printers (Small Label PDF).

## Non-Functional Requirements
- **Performance:** QR codes should be generated on-the-fly or stored efficiently.
- **Compatibility:** The PDF report must be compatible with standard label printers (e.g., Zebra, Dymo).
- **UX:** The QR code must be large enough to scan but not disrupt the form layout.

## Acceptance Criteria
- [ ] A QR code is visible at the top of the `inventory.asset` form.
- [ ] Scanning the QR code opens a web page/view with a preview of the asset's label.
- [ ] A button "Imprimir ID" exists below the QR code.
- [ ] Clicking "Imprimir ID" generates and downloads/opens a Small Label PDF.
- [ ] The generated PDF correctly displays the asset's `identificador_final`.

## Out of Scope
- Support for multiple label sizes or custom layouts.
- Bulk printing from the list view.
- Inclusion of the QR code itself on the *printed* label (unless specified otherwise).