# -*- coding: utf-8 -*-
{
    'name': "Planes Detallados de Trabajo",

    'summary': """
        Módulo para implementar planes detallados de trabajo""",

    'description': """
       Módulo para implementar planes detallados de trabajo
    """,
    'author': "Miguel Angel Suárez Benítez",
    'website': "https://www.escaesolutions.com",
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
        'views/checklist_menu.xml',
    ],


}
