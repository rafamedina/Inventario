from datetime import date

from odoo.tests import common



class TestMaintenanceChecklists(common.TransactionCase):
    def setUp(self):
        super(TestMaintenanceChecklists, self).setUp()
        self.MaintenancePlan = self.env["plans.asset"]
        self.MaintenanceTask = self.env["plans.task"]
        self.Category = self.env["inventory.category"]
        self.Subcategory = self.env["inventory.subcategory"]
        self.Asset = self.env["inventory.asset"]
        self.MaintenanceInstance = self.env["inventory.asset.maintenance"]

        # Setup basic data
        self.cat = self.Category.create({"nombre": "EQUIPOS", "codigo": "HW"})
        self.subcat = self.Subcategory.create({"nombre": "Laptop", "codigo": "LAP", "categoria_id": self.cat.id})

        # Create a plan with tasks
        self.plan = self.MaintenancePlan.create(
            {
                "nombre": "Plan Laptop Anual",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "tarea_ids": [
                    (0, 0, {"name": "Limpieza de ventiladores"}),
                    (0, 0, {"name": "Cambio de pasta térmica"}),
                ],
            }
        )

    def test_01_maintenance_instance_creation(self):
        """Test manual creation of maintenance instance and its lines"""
        asset = self.Asset.create(
            {
                "nombre": "Laptop Admin",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "plan_id": self.plan.id,
            }
        )

        instance = self.MaintenanceInstance.create(
            {
                "asset_id": asset.id,
                "plan_id": self.plan.id,
                "fecha_inicio": date.today(),
                "checklist_line_ids": [
                    (0, 0, {"name": "Tarea 1", "is_done": False}),
                    (0, 0, {"name": "Tarea 2", "is_done": True}),
                ],
            }
        )

        self.assertEqual(instance.asset_id.id, asset.id)
        self.assertEqual(len(instance.checklist_line_ids), 2)
        self.assertTrue(instance.checklist_line_ids[1].is_done)

    def test_02_start_maintenance_action(self):
        """Test that action_start_maintenance creates the instance from plan tasks"""
        asset = self.Asset.create(
            {
                "nombre": "Laptop Tech",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "plan_id": self.plan.id,
            }
        )

        # Iniciar mantenimiento
        asset.action_start_maintenance()

        self.assertEqual(asset.estado_mantenimiento_proceso, "en_proceso")
        self.assertTrue(asset.mantenimiento_activo_id)
        self.assertEqual(len(asset.mantenimiento_activo_id.checklist_line_ids), 2)
        self.assertEqual(
            asset.mantenimiento_activo_id.checklist_line_ids.mapped("name"),
            ["Limpieza de ventiladores", "Cambio de pasta térmica"],
        )

    def test_03_finish_maintenance_action(self):
        """Test that action_finish_maintenance updates status and history"""
        asset = self.Asset.create(
            {
                "nombre": "Laptop Boss",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "plan_id": self.plan.id,
            }
        )

        asset.action_start_maintenance()
        instance = asset.mantenimiento_activo_id

        # Marcar tareas como hechas
        for line in instance.checklist_line_ids:
            line.is_done = True

        # Finalizar mantenimiento
        asset.action_finish_maintenance()

        self.assertEqual(asset.estado_mantenimiento_proceso, "realizado")
        self.assertFalse(asset.mantenimiento_activo_id)
        self.assertEqual(len(asset.mantenimiento_history_ids), 1)
        self.assertEqual(asset.ultimomantenimiento, date.today())
        self.assertEqual(instance.state, "done")
        self.assertTrue(instance.fecha_fin)
