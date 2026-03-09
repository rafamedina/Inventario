import pytest
from odoo.tests.common import TransactionCase

@pytest.mark.unit
class TestAssetQR(TransactionCase):
    def setUp(self):
        super(TestAssetQR, self).setUp()
        self.category = self.env['inventory.category'].create({
            'nombre': 'Computadoras',
            'codigo': 'COMP'
        })
        self.subcategory = self.env['inventory.subcategory'].create({
            'nombre': 'Laptops',
            'codigo': 'LAP',
            'categoria_id': self.category.id
        })
        self.asset = self.env['inventory.asset'].create({
            'nombre': 'Laptop HP',
            'categoria_id': self.category.id,
            'subcategoria_id': self.subcategory.id
        })

    def test_qr_code_field_exists(self):
        """Verificar que el campo qr_code existe en el modelo."""
        self.assertIn('qr_code', self.env['inventory.asset']._fields)

    def test_qr_code_computation(self):
        """Verificar que el QR se genera correctamente."""
        self.assertTrue(self.asset.qr_code, "El QR debería haberse generado")

    def test_ui_elements_in_view(self):
        """Verificar que el QR NO está en la vista de formulario (se movió a etiquetas)."""
        view = self.env.ref('Inventario.view_inventory_asset_form')
        arch = view.arch
        self.assertNotIn('name="qr_code"', arch, "El QR ya no debería estar en la vista de formulario")

    def test_label_report_existence(self):
        """Verificar que el reporte de etiquetas existe."""
        report = self.env.ref('Inventario.action_report_asset_label')
        self.assertTrue(report, "El reporte de etiquetas debe existir")
