# Guía Completa: Sistema de CI/CD para Odoo 18

Este documento consolida toda la información necesaria para entender, gestionar y mantener el pipeline de Integración y Despliegue Continuo (CI/CD) del módulo de Inventario.

---

## 1. Explicación: Arquitectura y Lógica
Este apartado explica los conceptos y la lógica detrás del sistema.

### Propósito
El objetivo principal de este pipeline es actuar como un **guardián de calidad**. Garantiza que el código en la rama de producción (`18.0-pre-prod`) sea estable, seguro y esté libre de archivos innecesarios que solo tienen sentido en desarrollo.

### El Flujo de Trabajo (Workflow)
El sistema utiliza un flujo lineal de 5 etapas diseñadas para fallar rápido:
1.  **Validación de Estilo:** Verifica que el código sea legible y siga los estándares de Python.
2.  **Construcción Unificada:** Crea una única imagen Docker para todos los tests.
3.  **Pruebas de Aislamiento (Unit):** Verifica la lógica interna de los modelos.
4.  **Pruebas de Flujo (Integration):** Simula el comportamiento del usuario final usando Chrome.
5.  **Promoción y Limpieza:** "Destila" el código para la rama de producción.

### Lógica de "Promoción Limpia"
Implementa una **limpieza quirúrgica**. Los archivos de test, configuraciones de IA (`conductor/`) y flujos de GitHub se eliminan para que la rama `18.0-pre-prod` sea una versión pura del módulo, lista para el cliente final.

### Modelo de Seguridad
Opera bajo el principio de **"Cero Confianza"**: no se asumen contraseñas por defecto y toda la comunicación depende de secretos inyectados dinámicamente por GitHub.

---

## 2. Guías de Uso (How-to)
Instrucciones paso a paso para tareas comunes.

### Cómo configurar el secreto de Postgres
1.  Navega a tu repositorio en GitHub > **Settings**.
2.  Ve a **Secrets and variables** > **Actions**.
3.  Haz clic en **New repository secret**.
4.  **Name:** `POSTGRES_PASSWORD`.
5.  **Secret:** Tu contraseña (ej. `pepito123`).

### Cómo disparar un build manualmente
1.  Ve a la pestaña **Actions** en GitHub.
2.  Selecciona **Odoo Module CI/CD Professional**.
3.  Haz clic en **Run workflow**.

### Cómo leer los resultados de los tests
1.  Entra en la ejecución fallida y abre el Job **Unit Tests** o **Integration Tests**.
2.  Busca el paso **Analyze Test Results**.
3.  Verás el resumen de tests y conteo de errores críticos.

### Cómo descargar los logs completos
1.  En el "Summary" de la ejecución, busca la sección **Artifacts**.
2.  Descarga `unit-test-logs` o `integration-test-logs`.

---

## 3. Referencia Técnica
Detalles técnicos, variables y límites.

### Variables de Entorno
| Variable | Propósito | Valor por Defecto |
| :--- | :--- | :--- |
| `ODOO_DB` | Nombre base de la DB | `test_ci_db` |
| `POSTGRES_USER` | Usuario de base de datos | `odoo` |
| `POSTGRES_PASSWORD` | Contraseña (vía Secret) | (Sin fallback) |
| `DOCKER_IMAGE` | Nombre de la imagen | `odoo-inventario-test` |

### Etapas y Timeouts
| Job | Tiempo Máximo | Descripción |
| :--- | :--- | :--- |
| `lint` | 5 min | Análisis estático con Ruff. |
| `build` | 15 min | Construcción de Docker con cache GHA. |
| `test-unit` | 15 min | Odoo tests (excluyendo `-ui`). |
| `test-integration`| 20 min | Odoo tours con Chrome Headless. |
| `promote` | 10 min | Limpieza y Push a Pre-Prod. |

### Artefactos y Etiquetas
*   **Retención:** 1 día para imágenes, 7 días para logs.
*   **Tags:** `v18.0-build-${{ github.run_number }}`.
