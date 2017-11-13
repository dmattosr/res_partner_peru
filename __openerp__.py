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

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'res_partner_view.xml',
    ],
    'demo': [
    ],
}
