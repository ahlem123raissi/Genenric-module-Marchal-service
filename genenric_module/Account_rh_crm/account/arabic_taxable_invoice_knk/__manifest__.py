# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    "name": "Arabic Taxable Invoice",
    "version": "18.0.1.0",
    'license': 'OPL-1',
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "category": "Accounting/Accounting",
    "depends": [
        "account"
    ],
    "summary": "Arabic Taxable Invoice Module is the Invoice Receipt Layout which is printed in english as well as Arabic language to ensure customer's ease of readability and displays content in proper format ready to use for commercial purpose. | Invoice Report | Qweb Report | Taxable Invoice | Invoice Report | Arabic Invoice Report | Arabic Invoice | Arabic Invoice",
    "description": """
Arabic Taxable Invoice Module is the Invoice Receipt Layout which is printed in english as well as Arabic language to ensure customer's ease of readability and displays content in proper format ready to use for commercial purpose.
    """,
    "data": [
        "data/report_paperformat.xml",
        "report/account_report.xml",
        "views/invoice_report.xml",
        "views/account_move_views.xml",
        "views/res_company.xml",
    ],
    'images': [
        'static/description/banner.jpg'
    ],
    'installable': True
}
