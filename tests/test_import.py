from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import common


class TestInventoryAssetImport(common.TransactionCase):
    def setUp(self):
        super(TestInventoryAssetImport, self).setUp()
        self.cat = self.env["inventory.category"].create({"nombre": "Test Cat", "codigo": "TC"})

    def test_multi_create_unique_uuid(self):
        """Test that creating multiple assets at once generates unique UUIDs"""
        vals_list = [
            {"nombre": "Asset 1"},
            {"nombre": "Asset 2"},
            {"nombre": "Asset 3"},
        ]
        assets = self.env["inventory.asset"].create(vals_list)

        uuids = assets.mapped("uuid_activo")
        self.assertEqual(len(uuids), len(set(uuids)), f"UUIDs should be unique, got: {uuids}")
        self.assertNotIn("Nuevo", uuids, "UUIDs should not be 'Nuevo'")

    def test_plans_asset_multi_create_unique_id(self):
        """Test that creating multiple plans at once generates unique identifiers"""
        # Need a subcategory first
        subcat = self.env["inventory.subcategory"].create({"nombre": "Subcat 1", "codigo": "SC1", "categoria_id": self.cat.id})
        vals_list = [
            {
                "nombre": "Plan 1",
                "subcategoria_id": subcat.id,
                "categoria_id": self.cat.id,
            },
            {
                "nombre": "Plan 2",
                "subcategoria_id": subcat.id,
                "categoria_id": self.cat.id,
            },
        ]
        plans = self.env["plans.asset"].create(vals_list)

        ids = plans.mapped("identificador")
        self.assertEqual(len(ids), len(set(ids)), f"Plan IDs should be unique, got: {ids}")
        self.assertNotIn("Nuevo", ids, "Plan IDs should not be 'Nuevo'")

    def test_plans_alert_compute_name(self):
        """Test that PlansAlert computes its name correctly"""
        plan = self.env["plans.asset"].create(
            {
                "nombre": "Test Plan",
                "categoria_id": self.cat.id,
                "subcategoria_id": self.env["inventory.subcategory"].create({"nombre": "Sub", "codigo": "S", "categoria_id": self.cat.id}).id,
            }
        )
        alert_days = self.env["plans.alert"].create({"plan_id": plan.id, "valor": 5, "unidad": "days"})
        alert_weeks = self.env["plans.alert"].create({"plan_id": plan.id, "valor": 2, "unidad": "weeks"})

        self.assertEqual(alert_days.name, "5 Días antes")
        self.assertEqual(alert_weeks.name, "2 Semanas antes")

    def test_inventory_asset_compute_display_names(self):
        """Test responsible and owner display names"""
        employee = self.env["hr.employee"].create({"name": "John Doe"})
        dept = self.env["hr.department"].create({"name": "IT"})

        asset = self.env["inventory.asset"].create(
            {
                "nombre": "Asset Test",
                "tipo_responsable": "empleado",
                "responsable_empleado_id": employee.id,
                "tipo_propietario": "departamento",
                "propietario_departamento_id": dept.id,
            }
        )

        self.assertEqual(asset.responsable_display, "John Doe")
        self.assertEqual(asset.propietario_display, "IT")

        asset.write({"tipo_responsable": "departamento", "responsable_departamento_id": dept.id})
        self.assertEqual(asset.responsable_display, "IT")

    def test_inventory_asset_maintenance_state(self):
        """Test maintenance state computation"""
        hoy = fields.Date.today()
        asset = self.env["inventory.asset"].create({"nombre": "Maintenance Test"})

        self.assertEqual(asset.estado_mantenimiento, "normal")

        asset.proximo_mantenimiento = hoy - timedelta(days=1)
        self.assertEqual(asset.estado_mantenimiento, "vencido")

        asset.proximo_mantenimiento = hoy + timedelta(days=2)
        self.assertEqual(asset.estado_mantenimiento, "proximo")

    def test_inventory_asset_archive_unlink_restrictions(self):
        """Test archive and unlink restrictions with owners"""
        employee = self.env["hr.employee"].create({"name": "Owner"})
        asset = self.env["inventory.asset"].create(
            {
                "nombre": "Restricted Asset",
                "tipo_propietario": "empleado",
                "propietario_empleado_id": employee.id,
            }
        )

        with self.assertRaises(UserError):
            asset.action_archive()

        with self.assertRaises(UserError):
            asset.unlink()

        asset.write({"propietario_empleado_id": False})
        asset.action_archive()
        self.assertFalse(asset.active)
