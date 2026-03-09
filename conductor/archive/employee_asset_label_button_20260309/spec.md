# Specification: Employee Asset Label Button

## Overview

Add a custom "Label Block" (UI element) to the standard Odoo Employee form (`hr.employee`) that acts as a navigation button. This block will redirect the user to a custom view (the employee's asset profile/history) within the `Inventario` module. The implementation must be done entirely within the `Inventario` module using view inheritance, without modifying original Odoo modules directly.

## Functional Requirements

- **Location:** The "Label Block" will be added to the `hr.employee` form view.
- **Visuals:** The block will have a dashed border with dimensions approximately 100mm x 40mm.
- **Interaction:** Clicking the block (or a button within it) will trigger an action to redirect the user to the "Activos" view associated with that employee.
- **Redirection:** The target view is the custom "Activos" profile which shows the employee's current assets and asset history.

## Non-Functional Requirements

- **Modular Design:** Use XML inheritance in the `Inventario` module to extend the `hr.employee` form view.
- **Responsive:** Ensure the 100x40mm block fits reasonably within the Odoo form layout.
- **Maintainability:** Follow Odoo's standard for view inheritance.

## Acceptance Criteria

- [ ] The `hr.employee` form view displays the new 100x40mm dashed block.
- [ ] Clicking the block redirects the user to the correct "Activos" view for that specific employee.
- [ ] The implementation is contained within the `Inventario` module.
- [ ] No original Odoo source code is modified.

## Out of Scope

- Modifying the actual "Activos" view (assuming it already exists as stated).
- Printing the label (this track is for navigation).
- Adding this block to other modules.
