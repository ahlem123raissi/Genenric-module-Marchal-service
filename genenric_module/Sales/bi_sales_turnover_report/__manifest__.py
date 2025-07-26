# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales Turnover Fluctuation Report | Sales Turnover Analysis Report Odoo App',
    'version': '18.0.0.0',
    'category': 'Sales',
    'summary': 'Turnover fluctuation report sale turnover report sale target fluctuation report sale order line variation report income fluctuation report sales revenue report sale turnover variation revenue turnover report income variation report sale revenue fluctuation',
    'description' :"""
        Sales Turnover Fluctuation Odoo App helps the user to design sales strategies based on customer ordering patterns by generating a "Turnover Fluctuation" report for the selected date range and customers. Users can choose the option to generate a report above entered discrepancy percentage and turnover limit.
    """,
    'author': 'BROWSEINFO',
    'website': 'https://www.browseinfo.com/demo-request?app=bi_sales_turnover_report&version=18&edition=Community',
    'depends': ['base','sale_management'],
    'data': [
        'report/report.xml',
        'report/sales_turnover.xml',
        'security/ir.model.access.csv',
        'wizard/sales_turnover_fluctuation.xml',
    ],
    'license':'OPL-1',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.browseinfo.com/demo-request?app=bi_sales_turnover_report&version=18&edition=Community',
    "images":['static/description/Banner.gif'],
}
