from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    analytic_distribution = fields.Json(
        string='Analytic Distribution',
        help="Define the analytic distribution to be applied by default on this product."
    )
    analytic_precision = fields.Integer(
        string='Analytic Precision',
        default=2,
        help="Defines the number of decimal places for analytic distribution."
    )
