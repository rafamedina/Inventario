# Track Specification: Fix Missing hr_skills Dependency

## Overview

This track addresses the error `Missing model hr.employee.skill.report` that occurs when running tests for the `Inventario` module in Odoo 18. This model is part of the `hr_skills` module, and its absence during tests indicates a missing dependency.

## Type

Bug Fix

## Functional Requirements

1. **Dependency Update:** Add `hr_skills` to the `depends` list in `__manifest__.py`.
2. **Registry Verification:** Ensure that Odoo correctly loads the registry with the `hr_skills` model present.
3. **Test Stability:** Verify that all existing tests for `Inventario` pass without the missing model error.

## Non-Functional Requirements

- **Odoo Compatibility:** Maintain compatibility with Odoo 18 core modules.

## Acceptance Criteria

- [ ] The `Inventario` module manifest includes `hr_skills`.
- [ ] The command `odoo-bin -i Inventario --test-enable` (or equivalent) runs without the `Missing model hr.employee.skill.report` error.
- [ ] Existing functionality in `Inventario` remains unaffected.

## Out of Scope

- Implementing any new features related to skills or employees.
- Modifying core Odoo 18 code.
