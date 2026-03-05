# Implementation Plan: Maintenance Checklists and History

## Phase 1: Tracking Models and History [checkpoint: f3d9493]
- [x] Task: Modelo de Instancia de Mantenimiento (`inventory.asset.maintenance`)
    - [x] Escribir tests para la creación de instancias con sus líneas de checklist.
    - [x] Implementar el modelo `inventory.asset.maintenance` y sus líneas (`inventory.asset.maintenance.line`).
- [x] Task: Extensión de `inventory.asset` para seguimiento
    - [x] Añadir campos `estado_mantenimiento_proceso`, `mantenimiento_activo_id`.
    - [x] Configurar la relación `mantenimiento_history_ids` (One2many al historial).
- [x] Task: Security and Access Rights
    - [x] Define CRUD access for all module users in `ir.model.access.csv`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Modelos de Seguimiento y Historial' (Protocol in workflow.md)

## Phase 2: Lógica de Negocio (Checks e Imágenes) [checkpoint: f10cedc]
- [x] Task: Acción "Iniciar Mantenimiento"
    - [x] Escribir tests para la creación automática del checklist desde el plan.
    - [x] Implementar método `action_start_maintenance()` que copie las `tarea_ids` del plan a las líneas de la instancia.
- [x] Task: Acción "Finalizar Mantenimiento"
    - [x] Escribir tests para el archivado y actualización de fechas.
    - [x] Implementar método `action_finish_maintenance()` que marque el estado del activo como `realizado`, actualice la fecha del último mantenimiento y cierre la instancia.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Lógica de Negocio (Checks e Imágenes)' (Protocol in workflow.md)

## Phase 3: Interfaz de Usuario (UI) [checkpoint: f10cedc]
- [x] Task: Checklist interactivo en el Formulario del Producto
    - [x] Añadir sección/pestaña con el checklist activo (si existe).
    - [x] Configurar botones de acción ("Iniciar", "Finalizar").
- [x] Task: Pestaña de Historial de Mantenimientos
    - [x] Añadir pestaña "Historial de Mantenimientos" con la lista de instancias finalizadas.
    - [x] Permitir ver los detalles de cada mantenimiento pasado (incluyendo las fotos).
- [x] Task: Conductor - User Manual Verification 'Phase 3: Interfaz de Usuario (UI)' (Protocol in workflow.md)

## Phase 4: Final Polishing and Validation [checkpoint: f10cedc]
- [x] Task: Final UI Enhancements
    - [x] Add status badges to the product list/form to highlight active maintenances.
    - [x] Ensure historical records are user-friendly to browse.
- [x] Task: Comprehensive System Test
    - [x] Execute an end-to-end flow: Create template -> Assign to product -> Complete checklist -> Verify history.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Polishing and Validation' (Protocol in workflow.md)
