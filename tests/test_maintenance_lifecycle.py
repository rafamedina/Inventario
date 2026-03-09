from datetime import date, timedelta


from odoo import fields
from odoo.tests import common



class TestMaintenanceLifecycle(common.TransactionCase):
    def setUp(self):
        super(TestMaintenanceLifecycle, self).setUp()
        self.Category = self.env["inventory.category"]
        self.Subcategory = self.env["inventory.subcategory"]
        self.Location = self.env["inventory.location"]
        self.Plan = self.env["plans.asset"]
        self.Asset = self.env["inventory.asset"]
        self.Employee = self.env["hr.employee"]

        # Setup basic data
        self.cat = self.Category.create({"nombre": "EQUIPOS", "codigo": "HW"})
        self.subcat = self.Subcategory.create({"nombre": "Servidor", "codigo": "SRV", "categoria_id": self.cat.id})
        self.loc = self.Location.create({"nombre": "Data Center", "codigo": "DC"})

        # Create a maintenance plan: Monthly (30 days)
        self.plan = self.Plan.create(
            {
                "nombre": "Monthly Server Check",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "periodicidad": "30",
            }
        )

        # Create an employee with a user linked
        self.user = self.env["res.users"].create({"name": "Maintenance Tech", "login": "tech", "email": "tech@example.com"})
        self.tech = self.Employee.create({"name": "John Tech", "user_id": self.user.id})

        # Create the asset
        self.asset = self.Asset.create(
            {
                "nombre": "Main Server",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "ubicacion_id": self.loc.id,
                "plan_id": self.plan.id,
                "tipo_responsable": "empleado",
                "responsable_empleado_id": self.tech.id,
            }
        )

    def test_maintenance_alert_generation(self):
        """Test that check_maintenance_dates creates an activity when due"""
        hoy = date.today()

        # Case 1: Maintenance is due today
        self.asset.proximo_mantenimiento = hoy
        self.Asset.check_maintenance_dates()

        activities = self.env["mail.activity"].search([("res_id", "=", self.asset.id), ("res_model", "=", "inventory.asset")])
        self.assertTrue(activities, "An activity should have been created for maintenance due today")
        self.assertIn("¡Mantenimiento HOY!", activities[0].summary)

        # Case 2: Maintenance is due in the future (matching an alert)
        self.env["plans.alert"].create({"plan_id": self.plan.id, "valor": 1, "unidad": "weeks"})

        self.asset.proximo_mantenimiento = hoy + timedelta(days=7)
        self.Asset.check_maintenance_dates()

        new_activities = self.env["mail.activity"].search(
            [
                ("res_id", "=", self.asset.id),
                ("res_model", "=", "inventory.asset"),
                ("summary", "like", "Recordatorio"),
            ]
        )
        self.assertTrue(
            new_activities,
            "An alert activity should have been created for maintenance in 1 week",
        )

    def test_maintenance_done_flow(self):
        """Test that action_maintenance_done updates dates correctly"""
        hoy = fields.Date.today()
        self.asset.proximo_mantenimiento = hoy

        # Call the action
        self.asset.action_maintenance_done()

        self.assertEqual(self.asset.ultimomantenimiento, hoy, "Last maintenance date should be today")
        expected_next = hoy + timedelta(days=30)
        self.assertEqual(
            self.asset.proximo_mantenimiento,
            expected_next,
            "Next maintenance date should be in 30 days",
        )

        # Verify message post
        messages = self.asset.message_ids.mapped("body")
        self.assertTrue(
            any("Tarea completada" in m for m in messages),
            "A message should be posted when maintenance is done",
        )
