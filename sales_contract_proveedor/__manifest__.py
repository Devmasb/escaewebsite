# -*- coding: utf-8 -*-
{
    'name': "Lista de contratos como proveedor",

    'summary': """
        Lista de contratos de proveedor con el sector público/privado""",

    'description': """

    """,

    'author': "ESCAE",
    'website': "https://www.escae.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ESCAE',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/contrato_sequence.xml',
    ],
    'license': 'LGPL-3',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
