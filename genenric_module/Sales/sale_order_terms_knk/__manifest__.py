# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': "Default Terms & Conditions (Sale)",
    'version': '18.0.1.1',
    'category': 'Sales/Sales',
    'depends': ['sale_management'],
    'license': 'OPL-1',
    'author': "Kanak Infosystems LLP.",
    'website': "https://www.kanakinfosystems.com",
    'summary': '''Default Terms & Conditions (Sale) module is used to set Default Terms & Conditions on your Sale Orders and Sale Order report. In this module, the user can write and enable default terms & conditions in settings. After that when the user creates a quotation and Sale order, terms & conditions are automatically shown in the sale order as well as in the Sale order Report.''',
    'description': '''
        This module is used to set Default Terms & Conditions
        on your sale Orders and SO report | Default Terms & Condition in Sale Order | Default Terms in Sale Order | Default Condition in Sale Order.
        =================
    ''',
    'images': ['static/description/banner.jpg'],
    'data': [
        'views/sale_view.xml',
    ],
    'sequence': 1,
    'installable': True,
}
