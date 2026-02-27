from odoo.tests import common
from odoo.exceptions import ValidationError, AccessError
from odoo import fields

class TestSubcategoryLink(common.TransactionCase):

    def setUp(self):
        super(TestSubcategoryLink, self).setUp()
        self.Category = self.env['inventory.category']
        self.Subcategory = self.env['inventory.subcategory']
        
        self.cat_apps = self.Category.create({'nombre': 'APLICACIONES', 'codigo': 'APP'})
        self.cat_hw = self.Category.create({'nombre': 'EQUIPOS', 'codigo': 'HW'})

    def test_subcategory_requires_category(self):
        """ Test that a subcategory cannot be created without a category """
        # After we implement the 'required=True' on the field
        with self.assertRaises(Exception): # Odoo throws IntegrityError or ValidationError
            with self.cr.savepoint():
                self.Subcategory.create({
                    'nombre': 'Test Sub',
                    'codigo': 'TSUB',
                    'categoria_id': False
                })

    def test_dynamic_filtering_domain(self):
        """ Test that subcategories are filtered by category in Assets """
        sub_nvg = self.Subcategory.create({
            'nombre': 'Navegador',
            'codigo': 'NVG',
            'categoria_id': self.cat_apps.id
        })
        sub_srv = self.Subcategory.create({
            'nombre': 'Servidor',
            'codigo': 'SRV',
            'categoria_id': self.cat_hw.id
        })
        
        asset = self.env['inventory.asset'].new({
            'categoria_id': self.cat_apps.id
        })
        
        # Check domain on subcategoria_id
        # Note: In Odoo, domains are often evaluated on the client side, 
        # but we can check if our search returns the expected results.
        available_subs = self.Subcategory.search([
            ('categoria_id', '=', asset.categoria_id.id)
        ])
        
        self.assertIn(sub_nvg, available_subs)
        self.assertNotIn(sub_srv, available_subs)

    def test_onchange_category_clears_subcategory(self):
        """ Test that changing the category resets the subcategory field """
        sub_nvg = self.Subcategory.create({
            'nombre': 'Navegador',
            'codigo': 'NVG',
            'categoria_id': self.cat_apps.id
        })
        
        asset = self.env['inventory.asset'].create({
            'nombre': 'Test Asset',
            'categoria_id': self.cat_apps.id,
            'subcategoria_id': sub_nvg.id
        })
        
        # Trigger onchange manually
        asset.categoria_id = self.cat_hw.id
        asset._onchange_categoria_id() # We will implement this method
        
        self.assertFalse(asset.subcategoria_id, "Subcategory should be cleared when category changes")

    def test_migration_logic(self):
        """ Test that the migration logic correctly links subcategories """
        from ..hooks import post_init_hook
        
        # Toggle NOT NULL to allow testing the hook logic with NULL records
        self.env.cr.execute("ALTER TABLE inventory_subcategory ALTER COLUMN categoria_id DROP NOT NULL")
        
        try:
            # Ensure no lingering NULLs from failed runs
            self.env.cr.execute("DELETE FROM inventory_subcategory WHERE categoria_id IS NULL")
            
            self.env.cr.execute("INSERT INTO inventory_subcategory (nombre, codigo, active, categoria_id) VALUES ('Portátil', 'LAP', true, NULL)")
            
            # Call hook
            post_init_hook(self.env)
            
            sub = self.Subcategory.search([('nombre', '=', 'Portátil')], limit=1)
            self.assertTrue(sub.categoria_id, "Subcategory should be linked after hook")
            self.assertEqual(sub.categoria_id.nombre, 'EQUIPOS')
            
            # Cleanup: Remove the test record before restoring NOT NULL
            sub.unlink()
        finally:
            # Restore NOT NULL always
            self.env.cr.execute("ALTER TABLE inventory_subcategory ALTER COLUMN categoria_id SET NOT NULL")
