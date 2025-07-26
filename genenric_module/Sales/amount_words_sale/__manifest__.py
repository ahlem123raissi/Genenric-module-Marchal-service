{
    'name': "Sale Order Amount In Words",
    'version': '1.0.0',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'category': 'Sales',
    'author': 'Luna ERP Solutions',
    'website': "https://www.lunerpsolutions.com",
    'summary': "Convert and display the total amount in words on Sale Orders in both forms and reports.",
    'description': """
        This module adds functionality to display the total amount in words on the Sale Order form view as well as in the printed Sale Order report. 
        It is a useful feature for enhancing clarity in Sale Order documents and ensuring amounts are clearly understood.
    """,
    'data': [
        'views/sale_order_view.xml',  # Customized sale order form view with amount in words
        'report/sale_order_report.xml',  # Report template adjustments for amount in words
    ],
    'images': ['static/description/banner.png'],  # Add a banner image to make the module page more appealing
    'application': False,
    'installable': True,
    'auto_install': False,  # Ensures that the module won't be installed automatically
    'maintainer': 'Luna ERP Solutions',
}
