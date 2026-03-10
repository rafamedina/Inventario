from odoo.tests import common


class TestPlanDuplication(common.TransactionCase):
    def setUp(self):
        super(TestPlanDuplication, self).setUp()
        self.MaintenancePlan = self.env["plans.asset"]
        self.Category = self.env["inventory.category"]
        self.Subcategory = self.env["inventory.subcategory"]

        # Setup basic data
        self.cat = self.Category.create({"nombre": "EQUIPOS", "codigo": "HW"})
        self.subcat = self.Subcategory.create({"nombre": "Laptop", "codigo": "LAP", "categoria_id": self.cat.id})

        # Create a plan with tasks and alerts
        self.original_plan = self.MaintenancePlan.create(
            {
                "nombre": "Plan Original",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.subcat.id,
                "tarea_ids": [
                    (0, 0, {"name": "Tarea 1"}),
                    (0, 0, {"name": "Tarea 2"}),
                ],
                "alerta_ids": [
                    (0, 0, {"valor": 1, "unidad": "weeks"}),
                    (0, 0, {"valor": 3, "unidad": "days"}),
                ],
            }
        )

    def test_plan_duplication_with_related_records(self):
        """Verify that duplicating a plan also duplicates its tasks and alerts"""
        # Duplicate the plan
        duplicated_plan = self.original_plan.copy()

        # Verify basic fields are copied
        self.assertEqual(duplicated_plan.nombre, self.original_plan.nombre + " (copy)")
        self.assertEqual(duplicated_plan.categoria_id.id, self.original_plan.categoria_id.id)
        self.assertEqual(duplicated_plan.subcategoria_id.id, self.original_plan.subcategoria_id.id)

        # Verify tasks are duplicated (Current failing behavior: they are likely empty)
        self.assertEqual(
            len(duplicated_plan.tarea_ids),
            len(self.original_plan.tarea_ids),
            "Maintenance tasks should have been duplicated"
        )
        original_task_names = sorted(self.original_plan.tarea_ids.mapped("name"))
        duplicated_task_names = sorted(duplicated_plan.tarea_ids.mapped("name"))
        self.assertEqual(duplicated_task_names, original_task_names)

        # Verify alerts are duplicated
        self.assertEqual(
            len(duplicated_plan.alerta_ids),
            len(self.original_plan.alerta_ids),
            "Alerts should have been duplicated"
        )
        original_alert_vals = sorted(self.original_plan.alerta_ids.mapped("valor"))
        duplicated_alert_vals = sorted(duplicated_plan.alerta_ids.mapped("valor"))
        self.assertEqual(duplicated_alert_vals, original_alert_vals)

        # Ensure they are new records, not the same ones
        self.assertNotEqual(
            set(duplicated_plan.tarea_ids.ids),
            set(self.original_plan.tarea_ids.ids)
        )
        self.assertNotEqual(
            set(duplicated_plan.alerta_ids.ids),
            set(self.original_plan.alerta_ids.ids)
        )
