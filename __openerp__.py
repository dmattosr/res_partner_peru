# -*- coding: utf-8 -*-
{
    'name': "res_partner_peru",

    'summary': """
        Añade conexión con sunat/reniec""",

    'description': """
        Permite recibir los datos de sunat/reniec mediante el documento de identificación
    """,

    'author': "Daniel Mattos",
    'website': "http://www.py-devs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'res_partner_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
}