# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'atuto',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/auto_views.xml',
        'views/marque_views.xml',
        'views/model_views.xml',
        'views/type_views.xml',
        'views/option_views.xml',
        'views/auto_list_views.xml',
        'views/auto_menus.xml',
    ],
    'application': True,
}