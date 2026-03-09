# Implementation Plan: Employee Asset Label Button

## Phase 1: Research & Identification

- [x] Task: Identify the technical ID for the "Activos" view/action.
- [x] Task: Confirm the standard Odoo view ID for `hr.employee` (usually `hr.view_employee_form`).
- [x] Task: Conductor - User Manual Verification 'Research' (Protocol in workflow.md)

## Phase 2: Test Setup & Structural UI

- [x] Task: Write a failing test (Red Phase) to check for the existence of the custom block in the `hr.employee` view.
- [x] Task: Create the XML file `views/employee_view_extension.xml` and register it in `__manifest__.py`.
- [x] Task: Implement the basic XML inheritance to add a placeholder block in `hr.employee`.
- [x] Task: Verify the test passes (Green Phase).
- [x] Task: Conductor - User Manual Verification 'Test Setup & Structural UI' (Protocol in workflow.md)

## Phase 3: Visuals & Navigation

- [x] Task: Write a test (Red Phase) to verify that the block's CSS properties (100x40mm dashed) and the navigation action are present.
- [x] Task: Add CSS/Inline styles for the 100x40mm dashed border.
- [x] Task: Implement the redirection button/link inside the block that triggers the "Activos" action for the current employee.
- [x] Task: Verify the test passes (Green Phase).
- [x] Task: Conductor - User Manual Verification 'Visuals & Navigation' (Protocol in workflow.md)

## Phase 4: Final Validation

- [x] Task: Final UI check on mobile/responsive layouts.
- [x] Task: Conductor - User Manual Verification 'Employee Asset Label Button Final Check' (Protocol in workflow.md)
