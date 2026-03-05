# Specification: Asset Traceability and Employee Filtering

## Overview
Enhance the Asset Inventory module to provide robust bidirectional traceability. When an asset (like a laptop) is assigned, the system must record the full historical log. Users must be able to filter employees by their currently and historically assigned assets, and conversely, view all assets assigned to an employee (as owner or responsible) from within their record in the inventory module.

## Functional Requirements
- **Bidirectional Traceability:**
  - **Asset to Employee:** Maintain a full history of all past and current assignments for each asset.
  - **Employee to Asset:** From an employee's perspective (within the inventory context), allow filtering by all assets ever assigned to them.
- **Filtering Logic:**
  - **Employee View:** Add filters to find employees who:
    - Currently have an asset assigned.
    - Have historically had an asset assigned.
    - Have a specific type of asset assigned (e.g., "Laptops").
  - **Asset Roles:** Filters must distinguish between "Owner" (Propietario) and "Responsible" (Responsable).
- **User Interface:**
  - **Employee Form:** Add a dedicated "Assigned Assets" tab to the employee form (within the inventory context) showing a list of their current and past assets.
  - **Search View:** Enhance the employee search view with the new asset-based filters.

## Non-Functional Requirements
- Ensure database performance when querying historical assignment logs.
- Maintain consistency between the asset's current state and its historical records.
- **Strictly internal development:** All changes must be contained within this module and not touch anything outside.
- **Detailed code comments:** Include extensive comments in the code to explain each block and specific function.

## Acceptance Criteria
- [ ] An asset assignment creates a permanent log entry that remains even if the asset is reassigned.
- [ ] The employee search view allows filtering by "Has Assigned Asset" and "Has Historical Asset".
- [ ] Filtering an employee by "Owner" or "Responsible" correctly returns the corresponding assets.
- [ ] An employee's record features a tab listing all assets they are/were associated with.

## Out of Scope
- Automatic migration of old assignments that weren't logged using this new system (unless requested later).
- Integration with external HR systems outside of the existing Odoo `hr` dependency.