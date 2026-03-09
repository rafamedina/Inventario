# === EJECUCIÓN DE TESTS ===

docker-compose exec web odoo -d postgres --db_host=db --db_user=odoo --db_password=odoo -i Inventario --test-enable --stop-after-init --xmlrpc-port=8070

docker-compose exec web odoo -d postgres --db_host=db --db_user=odoo --db_password=odoo -i Inventario --test-enable --stop-after-init --xmlrpc-port=8070
