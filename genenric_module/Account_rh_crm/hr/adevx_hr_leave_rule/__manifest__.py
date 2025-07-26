{
    "name": "HR Leave Rule",
    "summary": "HR Leave Rule",
    "description": "HR Leave Rule",

    'author': 'Adevx',
    'category': 'Generic Modules/Human Resources',
    "license": "OPL-1",
    'website': 'https://adevx.com',
    "price": 0,
    "currency": 'USD',

    "depends": ["hr", 'hr_holidays'],
    "data": [
        # Security
        'security/ir.model.access.csv',
        # views
        "views/hr_leave_rule.xml",
        "views/hr_leave_type.xml",
        "views/hr_leave_allocation.xml",
    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
