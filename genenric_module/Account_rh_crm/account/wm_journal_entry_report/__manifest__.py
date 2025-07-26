# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Journal Entries Report',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': """Print Journal Entries pdf report.
    journal entry pdf
    print journal entry 
    print journal entry report
    account journal entry report
    journal report
    account entry report
    journal entry report
    """,
    'description': """Print Journal Entries pdf report.""",
    'license': 'LGPL-3',
    'price': 000,
    'currency': 'USD',
    'author': 'Waleed Mohsen',
    'support': 'mohsen.waleed@gmail.com',
    'depends': ['base', 'account'],
    'data': [
        'report/report_journal_entry.xml',
    ],
    'installable': True,
    'auto_install': False,
    "images": ["static/description/main_screenshot.png"],
}
