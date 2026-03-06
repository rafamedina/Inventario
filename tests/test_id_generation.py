from odoo.tests import common
from odoo import fields
import threading
import time

class TestIDGeneration(common.TransactionCase):

    def setUp(self):
        super(TestIDGeneration, self).setUp()
        self.cat = self.env['inventory.category'].create({'nombre': 'Test Cat', 'codigo': 'TC'})
        self.subcat = self.env['inventory.subcategory'].create({
            'nombre': 'Subcat 1', 
            'codigo': 'SC1',
            'categoria_id': self.cat.id
        })

    def test_plans_asset_sequence(self):
        """ Test that PlansAsset IDs follow the sequence format """
        plan1 = self.env['plans.asset'].create({
            'nombre': 'Plan 1', 
            'subcategoria_id': self.subcat.id, 
            'categoria_id': self.cat.id
        })
        plan2 = self.env['plans.asset'].create({
            'nombre': 'Plan 2', 
            'subcategoria_id': self.subcat.id, 
            'categoria_id': self.cat.id
        })
        
        self.assertTrue(plan1.identificador.startswith('PLAN-'), f"Expected prefix PLAN-, got {plan1.identificador}")
        self.assertTrue(plan2.identificador.startswith('PLAN-'), f"Expected prefix PLAN-, got {plan2.identificador}")
        
        # Check that they are sequential
        id1 = int(plan1.identificador.split('-')[1])
        id2 = int(plan2.identificador.split('-')[1])
        self.assertEqual(id2, id1 + 1, f"IDs should be sequential, got {id1} and {id2}")

    def test_inventory_asset_sequence(self):
        """ Test that InventoryAsset IDs (uuid_activo) follow the sequence format """
        asset1 = self.env['inventory.asset'].create({'nombre': 'Asset 1'})
        asset2 = self.env['inventory.asset'].create({'nombre': 'Asset 2'})
        
        self.assertTrue(asset1.uuid_activo.isdigit(), f"Expected numeric ID, got {asset1.uuid_activo}")
        self.assertTrue(asset2.uuid_activo.isdigit(), f"Expected numeric ID, got {asset2.uuid_activo}")
        
        # Check that they are sequential
        id1 = int(asset1.uuid_activo)
        id2 = int(asset2.uuid_activo)
        self.assertEqual(id2, id1 + 1, f"IDs should be sequential, got {id1} and {id2}")

    def test_manual_id_preservation(self):
        """ Test that manual IDs are preserved and don't trigger the sequence """
        asset = self.env['inventory.asset'].create({
            'nombre': 'Manual Asset',
            'uuid_activo': 'MANUAL-001'
        })
        self.assertEqual(asset.uuid_activo, 'MANUAL-001', "Manual UUID should be preserved")
        
        plan = self.env['plans.asset'].create({
            'nombre': 'Manual Plan',
            'categoria_id': self.cat.id,
            'subcategoria_id': self.subcat.id,
            'identificador': 'M-PLAN-01'
        })
        self.assertEqual(plan.identificador, 'M-PLAN-01', "Manual Identificador should be preserved")

    def test_identificador_final_computation(self):
        """ Test that the standardized ID (identificador_final) is computed correctly """
        # Create a location
        location = self.env['inventory.location'].create({'nombre': 'Test Location', 'codigo': 'TL'})
        
        # Create an asset with category, subcategory and location
        asset = self.env['inventory.asset'].create({
            'nombre': 'Standardized Asset',
            'categoria_id': self.cat.id,
            'subcategoria_id': self.subcat.id,
            'ubicacion_id': location.id,
            'anio_inclusion': '2026'
        })
        
        # Check identificador_final
        # cat.codigo = TC, subcat.codigo = SC1, location.codigo = TL, anio = 2026
        # uuid_activo is from sequence, e.g., '0003' if it's the 3rd asset created in this test run
        expected_start = "TC.SC1.TL."
        expected_end = ".2026"
        self.assertTrue(asset.identificador_final.startswith(expected_start), f"Expected prefix {expected_start}, got {asset.identificador_final}")
        self.assertTrue(asset.identificador_final.endswith(expected_end), f"Expected suffix {expected_end}, got {asset.identificador_final}")
        
        # Check fallback (XXX)
        asset_empty = self.env['inventory.asset'].create({'nombre': 'Empty Asset'})
        self.assertIn("XXX.XXX.XXX.", asset_empty.identificador_final, "Fallbacks should be XXX")
