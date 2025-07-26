{
    'name': "Product Analytic Account",
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add analytic account to products and auto-fill in invoice lines',
    'author': "Abdelrhman Ashraf",
    'website': "https://www.linkedin.com/in/abdelrhman1997/",
    'depends': [
        'product',
        'account',
        'sale',
        'purchase',
        'analytic',
    ],
    'data': [
        'views/product_views_analytic.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
