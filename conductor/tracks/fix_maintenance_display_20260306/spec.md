# Track: Fix maintenance display in asset form

## Overview
Currently, when a user attempts to assign a maintenance plan to an asset in the "Inventory Asset" form, the "Plan de Mantenimiento" (`plan_id`) dropdown remains empty, even if plans with the matching category and subcategory have been created. This prevents users from properly linking assets to their maintenance schedules.

## Functional Requirements
- The `plan_id` dropdown in the `inventory.asset` form must display all active `plans.asset` records that match the asset's current `subcategoria_id`.
- If the `subcategoria_id` is changed on the asset, the `plan_id` dropdown must be filtered accordingly.
- (Optional Improvement) If only `categoria_id` is selected but not `subcategoria_id`, the dropdown should ideally show all plans for that category.

## Non-Functional Requirements
- Ensure the domain evaluation is reactive in the Odoo web interface.
- Follow Odoo 18 best practices for dynamic domains in Many2one fields.

## Acceptance Criteria
1. Create an asset and assign a category and subcategory.
2. Create a maintenance plan for the same category and subcategory.
3. Open the asset form and verify the created plan appears in the `plan_id` dropdown.
4. Verify that changing the subcategory on the asset updates the available plans in the dropdown.

## Out of Scope
- Modifying the maintenance execution logic (`action_start_maintenance`, etc.).
- Changing the maintenance history view.
