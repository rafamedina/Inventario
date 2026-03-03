# Implementation Plan: Maintenance Checklists and History

## Phase 1: Tracking Models and History
- [x] Task: Modelo de Instancia de Mantenimiento (`inventory.asset.maintenance`)
    - [x] Escribir tests para la creación de instancias con sus líneas de checklist.
    - [x] Implementar el modelo `inventory.asset.maintenance` y sus líneas (`inventory.asset.maintenance.line`).
- [x] Task: Extensión de `inventory.asset` para seguimiento
    - [x] Añadir campos `estado_mantenimiento_proceso`, `mantenimiento_activo_id`.
    - [x] Configurar la relación `mantenimiento_history_ids` (One2many al historial).
- [x] Task: Security and Access Rights
    - [x] Define CRUD access for all module users in `ir.model.access.csv`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Modelos de Seguimiento y Historial' (Protocol in workflow.md)

## Phase 2: Lógica de Negocio (Checks e Imágenes)
- [ ] Task: Acción "Iniciar Mantenimiento"
    - [ ] Escribir tests para la creación automática del checklist desde el plan.
    - [ ] Implementar método `action_start_maintenance()` que copie las `tarea_ids` del plan a las líneas de la instancia.
- [ ] Task: Acción "Finalizar Mantenimiento"
    - [ ] Escribir tests para el archivado y actualización de fechas.
    - [ ] Implementar método `action_finish_maintenance()` que marque el estado del activo como `realizado`, actualice la fecha del último mantenimiento y cierre la instancia.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Lógica de Negocio (Checks e Imágenes)' (Protocol in workflow.md)

## Phase 3: Interfaz de Usuario (UI)
- [ ] Task: Checklist interactivo en el Formulario del Producto
    - [ ] Añadir sección/pestaña con el checklist activo (si existe).
    - [ ] Configurar botones de acción ("Iniciar", "Finalizar").
- [ ] Task: Pestaña de Historial de Mantenimientos
    - [ ] Añadir pestaña "Historial de Mantenimientos" con la lista de instancias finalizadas.
    - [ ] Permitir ver los detalles de cada mantenimiento pasado (incluyendo las fotos).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Interfaz de Usuario (UI)' (Protocol in workflow.md)

## Phase 4: Final Polishing and Validation
- [ ] Task: Final UI Enhancements
    - [ ] Add status badges to the product list/form to highlight active maintenances.
    - [ ] Ensure historical records are user-friendly to browse.
- [ ] Task: Comprehensive System Test
    - [ ] Execute an end-to-end flow: Create template -> Assign to product -> Complete checklist -> Verify history.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Polishing and Validation' (Protocol in workflow.md)
