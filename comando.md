python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons -d odoo


python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons -d odoo -i base   (reiniciar db)


python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons,module -d odoo -u Inventario (mantener vigilando mi modulo)

source venv/bin/activate



python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons,module -d odoo17_nueva -u Inventario

# === EJECUCIÓN DE TESTS ===
# Este comando ejecuta los tests del módulo y se detiene al terminar.
# Sintaxis:
python3 odoo-bin -r odoo -w odoo --db_host=localhost --addons-path=addons,module -d odoo --test-enable --stop-after-init -i Inventario

# Significado:
# --test-enable: Activa la ejecución de los archivos de la carpeta /tests.
# --stop-after-init: Detiene el proceso automáticamente al finalizar los tests (ideal para CI o desarrollo rápido).
# -i Inventario: Fuerza la instalación limpia y ejecución de todos los tests del módulo.
# --test-tags: (Opcional) Puedes añadirlo para filtrar tests específicos y ahorrar tiempo, ej: --test-tags=at_install
