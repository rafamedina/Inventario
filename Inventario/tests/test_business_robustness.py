from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
import psycopg2

class TestBusinessRobustness(TransactionCase):
    def setUp(self):
        super(TestBusinessRobustness, self).setUp()
        self.Category = self.env['inventory.category']
        self.Subcategory = self.env['inventory.subcategory']
        self.Location = self.env['inventory.location']
        self.Asset = self.env['inventory.asset']
        self.Maintenance = self.env['inventory.asset.maintenance']

        # Setup basic data
        self.cat = self.Category.create({'nombre': 'EQUIPOS', 'codigo': 'HW'})
        self.subcat = self.Subcategory.create({
            'nombre': 'Laptop',
            'codigo': 'LAP',
            'categoria_id': self.cat.id
        })
        self.loc = self.Location.create({'nombre': 'Oficina Central', 'codigo': 'OFC'})
        
        self.asset = self.Asset.create({
            'nombre': 'Laptop Admin',
            'categoria_id': self.cat.id,
            'subcategoria_id': self.subcat.id,
            'ubicacion_id': self.loc.id
        })

    def test_prevent_category_deletion_with_assets(self):
        """No se debe permitir borrar una categoría si tiene activos."""
        with self.assertRaises(UserError, msg="Debería prohibir el borrado de categoría con activos"):
            self.cat.unlink()

    def test_prevent_location_deletion_with_assets(self):
        """No se debe permitir borrar una ubicación si tiene activos."""
        with self.assertRaises(UserError, msg="Debería prohibir el borrado de ubicación con activos"):
            self.loc.unlink()

    def test_enforce_unique_asset_id(self):
        """Verificar que el identificador_final es único (SQL Constraint)."""
        # Forzamos el cálculo y guardado en DB
        self.asset._compute_identificador_final()
        self.env.cr.flush() # Flush to ensure ID is in DB
        
        with self.assertRaises(psycopg2.IntegrityError):
            with self.env.cr.savepoint():
                self.Asset.create({
                    'nombre': 'Laptop Duplicada',
                    'categoria_id': self.cat.id,
                    'subcategoria_id': self.subcat.id,
                    'ubicacion_id': self.loc.id,
                    'uuid_activo': self.asset.uuid_activo # Mismo UUID forzado
                })

    def test_restrict_done_maintenance_deletion(self):
        """No se debe permitir borrar mantenimientos en estado 'Hecho'."""
        plan = self.env['plans.asset'].create({
            'nombre': 'Plan Test',
            'categoria_id': self.cat.id,
            'subcategoria_id': self.subcat.id
        })
        maintenance = self.Maintenance.create({
            'asset_id': self.asset.id,
            'plan_id': plan.id,
            'state': 'done'
        })
        
        with self.assertRaises(UserError, msg="No se puede borrar un mantenimiento finalizado"):
            maintenance.unlink()
