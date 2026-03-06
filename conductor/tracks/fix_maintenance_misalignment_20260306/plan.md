# Implementation Plan - Fix visual misalignment in maintenance history

## Phase 1: Research & Reproduction
- [ ] Task: Research Odoo 18 `list` view constraints and widget options for `fields.Text` inside a Many2one/One2many list.
- [ ] Task: Create a failing test case (if applicable for UI) or a reproduction scenario description to identify the misalignment's root cause.
- [ ] Task: Conductor - User Manual Verification 'Research & Reproduction' (Protocol in workflow.md)

## Phase 2: UI Fix Implementation
- [ ] Task: Adjust the `notes` field definition and widget in `views/views.xml`.
- [ ] Task: Consider using `optional="show"` or a more compact widget (like `char` instead of `text` or a `char` field in the list) to prevent alignment issues.
- [ ] Task: Verify the fix by opening both the active maintenance and history tabs.
- [ ] Task: Conductor - User Manual Verification 'UI Fix Implementation' (Protocol in workflow.md)

## Phase 3: Finalization & Documentation
- [ ] Task: Run project linters and ensure code style adherence.
- [ ] Task: Conductor - User Manual Verification 'Finalization & Documentation' (Protocol in workflow.md)
