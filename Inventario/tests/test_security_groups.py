from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestSecurityGroups(TransactionCase):
    def test_security_group_creation(self):
        """Verificar que el grupo de seguridad se ha creado correctamente."""
        group = self.env.ref('Inventario.group_inventory_manager')
        self.assertTrue(group, "El grupo de seguridad 'Inventory / Full Access' no fue encontrado.")
        self.assertEqual(group.name, 'Inventory / Full Access')
        
        category = self.env.ref('Inventario.module_category_inventory')
        self.assertTrue(category, "La categoría del módulo no fue encontrada.")
        self.assertEqual(group.category_id.id, category.id)

    def test_group_users(self):
        """Verificar que el superusuario está en el grupo por defecto."""
        group = self.env.ref('Inventario.group_inventory_manager')
        admin_user = self.env.ref('base.user_admin')
        self.assertIn(admin_user, group.users, "El usuario administrador debería estar en el grupo.")

    def test_restricted_access(self):
        """Verificar que un usuario sin el grupo no puede acceder a los activos."""
        # Creamos un usuario normal sin el grupo de inventario
        user_no_access = self.env['res.users'].create({
            'name': 'Test User No Access',
            'login': 'test_no_access',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        
        # Intentamos leer un activo con ese usuario
        asset = self.env['inventory.asset'].create({'nombre': 'Asset Prueba'})
        
        with self.assertRaises(AccessError):
            asset.with_user(user_no_access).read(['nombre'])
