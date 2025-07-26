# -*- coding: utf-8 -*-
{
    'name': 'CRM to Sales Automation',
    'version': '18.0.0.0',
    'summary': """ Auto Sale Order & PO from CRM Leads | Stock-Based Procurement | CRM Lead to Sale Order & RFQ Automation | Odoo Inventory Sync """,
    'description': 
            """ Automatically convert CRM Leads to Sale Orders in Odoo and generate Purchase Orders (RFQs) when stock is low.
             Streamline sales & procurement with smart inventory-based automation to prevent stockouts and save time """,
    'author': 'Rifat Ahmed',
    'website': '',
    'category': 'Sales',
    'depends': ['crm', 'sale', 'stock', 'purchase'],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_product_line_views.xml",
        "views/crm_lead_views.xml",
        "reports/lead_stock_report.xml",
    ],
    'images':["static/description/banner.png"],
    # 'assets': {
    #           'web.assets_backend': [
    #               'lead_stock_manager/static/src/**/*'
    #           ],
    #       },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
