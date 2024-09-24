# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/types_views.xml',
        'views/tag_views.xml',
        'views/offer_type_views.xml',
        'views/test_model_views.xml',
        'views/user_view.xml',
        'views/test_model_list_views.xml',
        'views/types_views_list.xml',
        'views/offers_views.xml',
        'views/test_model_menus.xml',
    ],
    'application': True,
}