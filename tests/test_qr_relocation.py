import pytest
from odoo.tests import common, tagged

@pytest.mark.unit
@tagged('post_install', '-at_install', 'test_qr_relocation')
class TestQRRelocation(common.TransactionCase):

    def test_qr_code_removed_from_form_header(self):
        """ Test that the qr_code field is NOT in the form view header """
        view = self.env.ref('Inventario.view_inventory_asset_form')
        arch = view.get_combined_arch()
        # This test will FAIL initially because qr_code is currently in the header
        self.assertNotIn('name="qr_code"', arch, "QR code field should have been removed from the form view header")

    def test_qr_code_in_label_report(self):
        """ Test that the QR code is now present in the label report template """
        template = self.env.ref('Inventario.report_asset_label_template')
        arch = template.arch
        # Check for image tag with qr_code field
        self.assertIn('t-att-src="image_data_uri(o.qr_code)"', arch, "The label report template should contain an image tag for the QR code")
