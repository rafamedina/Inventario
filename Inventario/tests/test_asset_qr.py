from odoo.tests import common

class TestAssetQR(common.TransactionCase):

    def setUp(self):
        super(TestAssetQR, self).setUp()
        self.asset = self.env['inventory.asset'].create({
            'nombre': 'Test QR Asset',
        })

    def test_qr_code_field_exists(self):
        """ Test that the qr_code field exists on the model """
        self.assertIn('qr_code', self.env['inventory.asset']._fields, "Field 'qr_code' should exist on inventory.asset")

    def test_qr_code_computation(self):
        """ Test that the qr_code field is correctly computed """
        self.asset._compute_identificador_final() # Ensure ID is computed
        qr_value = self.asset.qr_code
        self.assertTrue(qr_value, "QR code should be computed")

    def test_label_report_existence(self):
        """ Test that the label report is defined and linked to the model """
        # This should fail in the Red phase
        report = self.env.ref('Inventario.action_report_asset_label', raise_if_not_found=False)
        self.assertTrue(report, "Report 'action_report_asset_label' should be defined")
        self.assertEqual(report.model, 'inventory.asset', "Report should be for 'inventory.asset' model")
