# Implementation Plan: Employee Asset Label Button

## Phase 1: Research & Identification
- [ ] Task: Identify the technical ID for the "Activos" view/action.
- [ ] Task: Confirm the standard Odoo view ID for `hr.employee` (usually `hr.view_employee_form`).
- [ ] Task: Conductor - User Manual Verification 'Research' (Protocol in workflow.md)

## Phase 2: Test Setup & Structural UI
- [ ] Task: Write a failing test (Red Phase) to check for the existence of the custom block in the `hr.employee` view.
- [ ] Task: Create the XML file `views/employee_view_extension.xml` and register it in `__manifest__.py`.
- [ ] Task: Implement the basic XML inheritance to add a placeholder block in `hr.employee`.
- [ ] Task: Verify the test passes (Green Phase).
- [ ] Task: Conductor - User Manual Verification 'Test Setup & Structural UI' (Protocol in workflow.md)

## Phase 3: Visuals & Navigation
- [ ] Task: Write a test (Red Phase) to verify that the block's CSS properties (100x40mm dashed) and the navigation action are present.
- [ ] Task: Add CSS/Inline styles for the 100x40mm dashed border.
- [ ] Task: Implement the redirection button/link inside the block that triggers the "Activos" action for the current employee.
- [ ] Task: Verify the test passes (Green Phase).
- [ ] Task: Conductor - User Manual Verification 'Visuals & Navigation' (Protocol in workflow.md)

## Phase 4: Final Validation
- [ ] Task: Final UI check on mobile/responsive layouts.
- [ ] Task: Conductor - User Manual Verification 'Employee Asset Label Button Final Check' (Protocol in workflow.md)
