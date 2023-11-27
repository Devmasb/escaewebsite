# -*- coding: utf-8 -*-
{
    'name': "Planes ",

    'summary': """
        Módulo para implementar planes detallados de trabajo""",

    'description': """
       Módulo para implementar planes detallados de trabajo
    """,

    'author': "Miguel Angel Suárez Benítez",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','documents','documents_project'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        'views/project_views.xml',
    ],
    'images': [
        'static/description/banner.gif',
    ],

}
