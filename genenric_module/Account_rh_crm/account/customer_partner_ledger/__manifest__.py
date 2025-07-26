{
    'name': 'Customer / Vendor (Partner) Ledger Report',
    
    'version': '1.0',
    
    'category': 'Accounting',
    
    'summary': 'Generate a detailed ledger report for customers and vendors.',

    'description': """
        This module enables you to generate a detailed ledger report for your customers and vendors, and gives you a closing balance. For instances where you use opening balances, it takes that into account as well when generating the report.
    """,
    
    'author': 'SIMI Technologies',
    
    'website': 'https://simitechnologies.co.ke',
    
    'depends': ['account'],
    
    'data': [
        'security/ir.model.access.csv',

        'views/customer_ledger_wizard_view.xml',
        
        'reports/customer_ledger_template.xml',
    ],

    'installable': True,

    'application': False,
    
    'license': 'LGPL-3',

    'images': ['static/description/images/cover.png'],
}
