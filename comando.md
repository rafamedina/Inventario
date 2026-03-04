python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons -d odoo


python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons -d odoo -i base   (reiniciar db)


python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons,module -d odoo -u Inventario (mantener vigilando mi modulo)

source venv/bin/activate





# === EJECUCIÓN DE TESTS ===
# Este comando ejecuta los tests del módulo y se detiene al terminar.
# Sintaxis:
python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons,module -d odoo --test-enable --stop-after-init -i Inventario

# Significado:
# --test-enable: Activa la ejecución de los archivos de la carpeta /tests.
# --stop-after-init: Detiene el proceso automáticamente al finalizar los tests (ideal para CI o desarrollo rápido).
# -i Inventario: Fuerza la instalación limpia y ejecución de todos los tests del módulo.
# --test-tags: (Opcional) Puedes añadirlo para filtrar tests específicos y ahorrar tiempo, ej: --test-tags=at_install



  1. Auditoría de Seguridad Global (/security:analyze)
  Este comando es parte de una extensión especializada y hace lo
  siguiente para todo el módulo:
   * Busca secretos hardcodeados (claves, contraseñas).
   * Analiza vulnerabilidades de inyección (SQL, Command
     Injection).
   * Busca fallos de control de acceso (IDOR, escalada de
     privilegios).
   * Detecta fugas de privacidad (datos personales en logs).
   * Genera un informe detallado de riesgos.


  2. Revisión de Código Estándar (/code-review)
  Este comando realiza una revisión más tradicional de "limpieza":
   * Evalúa la calidad del código según las guías del proyecto.
   * Busca redundancias o falta de optimización.
   * Es ideal si quieres un "segundo par de ojos" sobre todo lo que
     se ha escrito en el módulo hasta ahora, no solo sobre un track
     específico.


  3. Verificación de Integridad Global (Manual con mis
  herramientas)

  Si quieres, puedo ejecutar una auditoría ad-hoc combinando mis
  capacidades:
   * Puedo ejecutar todos los tests del módulo a la vez para ver si
     hay conflictos entre diferentes funciones.
   * Puedo buscar patrones específicos (como todos los menús que no
     tengan grupo) para asegurar consistencia.

     
     /home/ikran/odooInventario17/.venv/bin/python3 \
/home/ikran/odooInventario17/odoo-bin -r odoo -w odoo \
--db_host=localhost --addons-path=addons,custom_modules \
-d odoo17_nueva_pro -i stock --test-enable --stop-after-init