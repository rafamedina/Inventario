# Specification: Plan Duplication with Checks and Alerts

## Overview

Currently, duplicating a maintenance plan (`plans.asset`) only copies the main record's fields, leaving the associated maintenance tasks (`tarea_ids`) and alerts (`alerta_ids`) empty. This track aims to extend the standard Odoo duplication behavior to include these related records, ensuring a complete copy of the plan is created.

## Functional Requirements

1. **Extend Duplication Logic:** Override the `copy()` method of the `plans.asset` model to handle deep copying of related records.
2. **Duplicate Maintenance Tasks:** Ensure that all tasks associated with the original plan (`tarea_ids`) are duplicated and linked to the new plan instance.
3. **Duplicate Alerts:** Ensure that all alerts associated with the original plan (`alerta_ids`) are duplicated and linked to the new plan instance.
4. **Standard Integration:** This behavior must trigger automatically when a user selects the standard Odoo "Duplicate" action on a plan record.

## Non-Functional Requirements

- **Performance:** Duplication should remain efficient even for plans with many tasks or alerts.
- **Integrity:** Ensure that IDs for the new related records are unique and correctly linked to the new parent plan.

## Acceptance Criteria

- [ ] Duplicating a plan results in a new plan with the same maintenance tasks as the original.
- [ ] Duplicating a plan results in a new plan with the same alerts as the original.
- [ ] The new plan's `identificador` is unique (handled by existing sequence logic in `create`).
- [ ] No errors occur during the duplication process.

## Out of Scope

- Custom duplication buttons or wizards.
- Duplication of maintenance _instances_ (only the _plans_ themselves are in scope).
