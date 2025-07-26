from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_amount_to_words(self):
        for order in self:
            order.amount_words_sale = str(order.currency_id.amount_to_text(order.amount_total)) + " Only"

    amount_words_sale = fields.Char(string="Total(In words):", compute='_compute_amount_to_words')
