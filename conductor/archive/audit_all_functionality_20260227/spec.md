# Specification: Audit all functionality

## Goal
The goal of this track is to perform a comprehensive audit of the "Inventario" Odoo module to ensure that all core features are functioning correctly according to the current requirements and code implementation.

## Scope
- **Models**: Verify that `inventory.category`, `inventory.subcategory`, `inventory.location`, `plans.asset`, `plans.task`, `plans.alert`, and `inventory.asset` are correctly defined and relate to each other as intended.
- **Data**: Ensure that the sequence data in `data/ir_sequence_data.xml` is correctly loaded and functioning.
- **Security**: Validate that `security/ir.model.access.csv` provides appropriate access rights.
- **Business Logic**:
    - Asset ID generation (`identificador_final`).
    - Maintenance alert logic (`check_maintenance_dates`).
    - Maintenance completion flow (`action_maintenance_done`).
- **Tests**: Verify that existing tests pass and add new ones if gaps are found.

## Acceptance Criteria
- [ ] All existing tests pass.
- [ ] New assets can be created with correctly generated standardized IDs.
- [ ] Subcategories are correctly linked to categories and filtered in the UI (domain check).
- [ ] Maintenance activities are correctly generated for assets reaching their maintenance date.
- [ ] Maintenance completion correctly updates the last and next maintenance dates.
- [ ] Archiving/Unlinking logic works as expected (preventing archival if owned).
