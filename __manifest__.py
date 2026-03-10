{
    "name": "Modulo de inventario de Wavext",
    "summary": "Administra el inventario de activos de la compañia Wavext",
    "description": """
Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "hr", "hr_skills"],
    # always loaded
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/templates.xml",
        "views/views.xml",
        "views/cron.xml",
        "views/employee_view_extension.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "post_init_hook": "post_init_hook",
}
