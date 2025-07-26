# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2024 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

{
    'name': "Stock Inventory Zones",
    'category': 'Warehouse',
    'version': '1.0',
    'summary': """
        Assign and filter the locations in the inventory adjustment based on the inventory zones.
    """,
    'website': 'https://sprintit.fi/in-english',
    'author': "SprintIT",
    'maintainer': 'SprintIT',
    'license': 'Other proprietary',
    'images': ['static/description/cover.jpg',],
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_inventory_zones.xml',
        'views/stock_location.xml',
        'views/stock_inventory.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
    'price': 0.0,
    'currency': 'EUR',
}