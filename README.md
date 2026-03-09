# Módulo de Inventario - Control de Acceso

Este módulo implementa un sistema de roles para restringir el acceso a la gestión de activos.

## Grupos de Seguridad

### Inventory / Full Access

- **ID Interno:** `Inventario.group_inventory_manager`
- **Permisos:** Control total (Lectura, Escritura, Creación, Eliminación) sobre todos los modelos del módulo (Activos, Categorías, Ubicaciones, Mantenimientos).
- **Visibilidad:** Solo los usuarios en este grupo pueden ver el icono del módulo "Gestión de Activos" en el tablero principal y la pestaña de activos en la ficha del empleado.

## Cómo otorgar acceso

Para dar acceso a un usuario al módulo de inventario:

1. Inicie sesión como **Administrador** de Odoo.
2. Vaya a **Ajustes > Usuarios y compañías > Usuarios**.
3. Seleccione al usuario que desea autorizar.
4. En la pestaña **Permisos**, busque la sección **Gestión de Inventario**.
5. Seleccione la opción **Inventory / Full Access** en el menú desplegable.
6. Guarde los cambios.

**Nota:** Si el usuario no tiene este permiso, el módulo será completamente invisible para él.
