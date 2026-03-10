from odoo.tests import common
from odoo import fields

class TestMaintenanceChatter(common.TransactionCase):
    def setUp(self):
        super(TestMaintenanceChatter, self).setUp()
        self.Category = self.env["inventory.category"]
        self.Subcategory = self.env["inventory.subcategory"]
        self.Location = self.env["inventory.location"]
        self.Asset = self.env["inventory.asset"]
        self.Maintenance = self.env["inventory.asset.maintenance"]
        self.MaintenanceLine = self.env["inventory.asset.maintenance.line"]

        # Setup basic data
        self.cat = self.Category.create({"nombre": "TEST", "codigo": "T"})
        self.subcat = self.Subcategory.create({"nombre": "TEST", "codigo": "T", "categoria_id": self.cat.id})
        self.loc = self.Location.create({"nombre": "TEST", "codigo": "T"})

        self.asset = self.Asset.create({
            "nombre": "Test Asset",
            "categoria_id": self.cat.id,
            "subcategoria_id": self.subcat.id,
            "ubicacion_id": self.loc.id,
        })

        # Create a maintenance record and mark it as done
        self.maintenance = self.Maintenance.create({
            "asset_id": self.asset.id,
            "state": "done",
            "fecha_inicio": fields.Date.today(),
            "fecha_fin": fields.Date.today(),
        })

        self.line = self.MaintenanceLine.create({
            "maintenance_id": self.maintenance.id,
            "name": "Task 1",
            "is_done": True,
            "notes": "Initial notes",
        })

    def test_maintenance_line_tracking_implemented(self):
        """Verify that changing notes on a line posts to parent chatter"""
        # Get initial message count
        initial_message_count = len(self.maintenance.message_ids)

        # Change notes
        self.line.write({"notes": "Updated notes after completion"})

        # Verify a new message was posted to the maintenance record
        new_message_count = len(self.maintenance.message_ids)
        self.assertGreater(
            new_message_count, 
            initial_message_count, 
            "Should have posted a message to the parent chatter"
        )
        
        # Verify message content
        last_message = self.maintenance.message_ids[0].body
        self.assertIn("Notas de 'Task 1' cambiadas", last_message)
        self.assertIn("Updated notes after completion", last_message)

    def test_maintenance_general_notes_tracking(self):
        """Verify that changing general notes on the maintenance record is tracked"""
        # Get initial message count
        initial_message_count = len(self.maintenance.message_ids)

        # Change general notes
        self.maintenance.write({"notas_generales": "Some general notes added"})

        # Standard tracking usually creates a message
        new_message_count = len(self.maintenance.message_ids)
        self.assertGreater(
            new_message_count, 
            initial_message_count, 
            "Should have tracked general notes change"
        )
