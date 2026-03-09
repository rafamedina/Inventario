import pytest
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

@pytest.mark.unit
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
        
        # Intentamos crear un activo con ese usuario
        # (Usamos sudo() para crear el registro inicial, luego probamos acceso)
        asset = self.env['inventory.asset'].sudo().create({'nombre': 'Asset Prueba'})
        
        with self.assertRaises(AccessError):
            asset.with_user(user_no_access).read(['nombre'])

    def test_granted_access(self):
        """Verificar que un usuario con el grupo SI puede acceder a los activos."""
        # Creamos un usuario con el grupo de inventario
        user_access = self.env['res.users'].create({
            'name': 'Test User Access',
            'login': 'test_access',
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('Inventario.group_inventory_manager').id
            ])]
        })
        
        # Intentamos leer un activo con ese usuario
        asset = self.env['inventory.asset'].sudo().create({'nombre': 'Asset Prueba'})
        
        # Esto NO debería lanzar AccessError
        res = asset.with_user(user_access).read(['nombre'])
        self.assertEqual(res[0]['nombre'], 'Asset Prueba')

    def test_menu_visibility(self):
        """Verificar que el menú raíz solo es visible para el grupo manager."""
        menu = self.env.ref('Inventario.menu_inventory_root')
        
        user_no_access = self.env['res.users'].create({
            'name': 'Menu No Access',
            'login': 'menu_no_access',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        
        user_access = self.env['res.users'].create({
            'name': 'Menu Access',
            'login': 'menu_access',
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('Inventario.group_inventory_manager').id
            ])]
        })

        # Verificar visibilidad (Odoo filtra los menús en la carga del cliente, 
        # pero podemos verificar si el usuario tiene el grupo requerido)
        self.assertFalse(menu.with_user(user_no_access)._filter_visible_menus(), 
                         "El menú NO debería ser visible para un usuario sin el grupo.")
        
        self.assertTrue(menu.with_user(user_access)._filter_visible_menus(), 
                        "El menú DEBERÍA ser visible para un usuario con el grupo.")
