from odoo.tests import common
from odoo import tools

class TestEmployeeAssetLabelUI(common.TransactionCase):

    def test_employee_form_contains_asset_smart_button(self):
        """ Test that the hr.employee form view has been extended with the asset smart button """
        employee_model = self.env['hr.employee']
        
        # Check standard view
        view_info = employee_model.get_view(view_id=self.env.ref('hr.view_employee_form').id)
        arch = view_info['arch']
        
        # Look for the smart button triggering the method
        self.assertIn('name="action_view_employee_assets"', arch, "The smart button should call 'action_view_employee_assets'")
        self.assertIn('class="oe_stat_button"', arch, "The button should have the 'oe_stat_button' class")
        self.assertIn('icon="fa-barcode"', arch, "The button should have the 'fa-barcode' icon")
        self.assertIn('field name="asset_count"', arch, "The button should display the asset_count field")

    def test_asset_count_computation(self):
        """ Test that asset_count is correctly computed for an employee """
        # Create an employee
        employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        
        # Create a category
        category = self.env['inventory.category'].create({'nombre': 'Cat', 'codigo': 'CAT'})
        
        # Create assets
        asset1 = self.env['inventory.asset'].create({
            'nombre': 'Asset 1',
            'categoria_id': category.id,
            'responsable_empleado_id': employee.id
        })
        asset2 = self.env['inventory.asset'].create({
            'nombre': 'Asset 2',
            'categoria_id': category.id,
            'propietario_empleado_id': employee.id
        })
        
        employee._compute_asset_count()
        self.assertEqual(employee.asset_count, 2, "The employee should have 2 assets")
