# Track: Maintenance Checklists and History

## Overview
This track implements a structured maintenance system for assets in the Inventory module. It introduces "Maintenance Plans" (reusable templates) with specific "Checklist Items" (e.g., 'Clean fans', 'Apply thermal paste'). When a plan is assigned to a product, it generates a task-based checklist that users can complete. The system supports uploading images for each task and tracks the maintenance status ('In Progress', 'Done'). All historical maintenances are stored and accessible directly from the product record.

## Functional Requirements
### 1. Maintenance Templates
- **Model:** `maintenance.plan`
- **Fields:**
    - `name`: Name of the plan (e.g., "Annual Laptop Maintenance").
    - `description`: Detailed description.
    - `item_ids`: One2many relationship to `maintenance.plan.item`.
- **Checklist Item Model:** `maintenance.plan.item`
    - `name`: Task description.
    - `sequence`: Order of the task.

### 2. Product Maintenance Assignment
- Products can have multiple `maintenance.plan` templates assigned.
- Assigning a plan creates a `product.maintenance.instance` for the product.
- **Maintenance Instance Model:** `product.maintenance.instance`
    - `product_id`: Reference to the asset.
    - `plan_id`: Reference to the template.
    - `status`: Selection ('in_progress', 'done').
    - `checklist_ids`: One2many to `product.maintenance.item` (instantiated from the template).
    - `assigned_date`: Date when the maintenance was initiated.
    - `completed_date`: Date when status changed to 'done'.

### 3. Interactive Checklist
- **Checklist Item Model (Instance):** `product.maintenance.item`
    - `name`: Copied from template.
    - `is_done`: Boolean to mark completion.
    - `image`: Binary field to upload proof of work.
    - `sequence`: Ordering.
- Users can check/uncheck items and upload images for each specific task.

### 4. Status Tracking
- A maintenance instance is 'In Progress' by default.
- Once all checklist items are marked `is_done`, the instance status can be set to 'Done'.
- Products should show their current maintenance status.

### 5. Historical Logs
- A new tab "Maintenance History" in the Product view.
- This tab lists all `product.maintenance.instance` records related to the product.
- Users can click on a historical record to view the checklist, images, and completion dates.

## Acceptance Criteria
- [ ] Admins can create Maintenance Plan templates with multiple items.
- [ ] Users can assign a plan to a product, creating an active checklist.
- [ ] Users can mark items as done and upload at least one image per item.
- [ ] Multiple plans can be active for the same product.
- [ ] Completed maintenances are moved to history and remain accessible.
- [ ] All users with module access can interact with the checklists.
