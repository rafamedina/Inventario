from odoo.tests import common

class TestEmployeeHistoryUI(common.TransactionCase):

    def setUp(self):
        super(TestEmployeeHistoryUI, self).setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.category = self.env['inventory.category'].create({'nombre': 'CAT', 'codigo': 'CAT'})
        self.subcategory = self.env['inventory.subcategory'].create({
            'nombre': 'SUB', 
            'codigo': 'SUB', 
            'categoria_id': self.category.id
        })
        self.location = self.env['inventory.location'].create({'nombre': 'LOC', 'codigo': 'LOC'})
        
        self.asset = self.env['inventory.asset'].create({
            'nombre': 'Test Asset',
            'categoria_id': self.category.id,
            'subcategoria_id': self.subcategory.id,
            'ubicacion_id': self.location.id,
            'responsable_empleado_id': self.employee.id,
        })

    def test_history_shows_asset_identifier(self):
        """ Test that history record can provide the asset's standardized ID """
        history = self.env['inventory.asset.history'].search([
            ('asset_id', '=', self.asset.id)
        ], limit=1)
        
        self.assertTrue(history.exists(), "History record should exist")
        
        # This is what we want to display in the UI
        # We can check if the field exists or if we can access it via dot notation
        # In Odoo XML tree views, we can use <field name="asset_id"/> and it shows the name.
        # If we want the ID, we might need a related field for better XML handling if dot notation fails in some widgets.
        
        expected_id = self.asset.identificador_final
        self.assertEqual(history.asset_id.identificador_final, expected_id)
