import pytest
from odoo.tests import common
from odoo.exceptions import AccessError

@pytest.mark.integration
class TestAssetTraceability(common.TransactionCase):

    def setUp(self):
        super(TestAssetAssetTraceability, self).setUp()
        # Create some employees for testing
        self.employee_1 = self.env['hr.employee'].create({'name': 'Employee 1'})
        self.employee_2 = self.env['hr.employee'].create({'name': 'Employee 2'})
        
        # Create an asset
        self.asset = self.env['inventory.asset'].create({
            'nombre': 'Test Laptop',
            'tipo_responsable': 'empleado',
            'responsable_empleado_id': self.employee_1.id,
            'tipo_propietario': 'empleado',
            'propietario_empleado_id': self.employee_1.id,
        })

    def test_history_model_existence(self):
        """ Test that the inventory.asset.history model exists and can be created """
        # This should FAIL in the Red phase as the model is not yet defined
        history = self.env['inventory.asset.history'].create({
            'asset_id': self.asset.id,
            'old_employee_id': self.employee_1.id,
            'new_employee_id': self.employee_2.id,
            'role': 'responsible',
            'date': '2026-02-27',
        })
        self.assertTrue(history.exists(), "History record should be created")

    def test_auto_history_logging(self):
        """ Test that changing an asset's responsible/owner triggers history logging """
        self.asset.write({'responsable_empleado_id': self.employee_2.id})
        
        # We expect 2 records now: the initial one from create() and the new one from write()
        history = self.env['inventory.asset.history'].search([
            ('asset_id', '=', self.asset.id),
            ('role', '=', 'responsible')
        ], order='id desc', limit=1) # Get the latest one
        
        self.assertTrue(history.exists(), "Automatic history record should be created on responsible change")
        self.assertEqual(history.old_employee_id.id, self.employee_1.id)
        self.assertEqual(history.new_employee_id.id, self.employee_2.id)

    def test_employee_inheritance(self):
        """ Test that hr.employee has fields to track assigned assets """
        # This should FAIL because the hr.employee inheritance is not implemented yet
        self.asset.write({'responsable_empleado_id': self.employee_1.id})
        
        # Check current assignments (assuming we add these fields)
        self.assertIn(self.asset, self.employee_1.current_responsible_asset_ids, "Asset should be in current responsible list")
        
        # Check historical assignments
        self.asset.write({'responsable_empleado_id': self.employee_2.id})
        self.assertIn(self.asset, self.employee_1.historical_asset_ids, "Asset should be in historical list for Employee 1")
