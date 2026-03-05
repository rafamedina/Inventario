from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    """
    Link existing subcategories to their parent categories based on nomenclature.
    """
    mapping = {
        'APLICACIONES': ['Navegador', 'Productividad', 'Utilidad', 'Inteligencia Artificial', 'Gestor de contraseñas', 'Correo electrónico', 'Escritorio remoto', 'Seguridad y antivirus', 'Comunicación y RRSS'],
        'EQUIPOS': ['Servidor', 'Impresora', 'Sobremesa', 'Portátil', 'Móvil', 'Tablet'],
        'COMUNICACIONES': ['Router', 'ISP / Proveedor', 'Red principal', 'Subred / VLAN'],
        'SOPORTES DE INFORMACIÓN': ['Físico', 'Digital'],
        'INFORMACIÓN': ['Documento', 'Base de datos', 'Dataset o fichero'],
        'INSTALACIONES': ['Oficina / Sede', 'Centro de datos', 'Cloud AWS', 'Cloud Microsoft', 'Cloud Ionos', 'Cloud otros'],
        'PERSONAL': ['Dirección', 'IT', 'RRHH', 'Marketing y Comunicación', 'Administración'],
        'PROCESOS Y SERVICIOS': ['Procedimiento interno', 'Política', 'Servicio externo', 'Servicio externo IT'],
        'SOFTWARE BASE / S.O.': ['ERP', 'Sistema operativo', 'Base de datos'],
        'ORGANIZACIÓN Y GOBIERNO': ['Estructura', 'Procesos', 'Gobierno corporativo'],
    }

    Category = env['inventory.category']
    Subcategory = env['inventory.subcategory']

    for cat_name, sub_names in mapping.items():
        category = Category.search([('nombre', '=', cat_name)], limit=1)
        if category:
            subcategories = Subcategory.search([('nombre', 'in', sub_names), ('categoria_id', '=', False)])
            if subcategories:
                subcategories.write({'categoria_id': category.id})
