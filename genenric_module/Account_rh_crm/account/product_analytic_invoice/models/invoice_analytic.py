from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('product_id')
    def _onchange_product_id_analytic(self):
        if self.product_id and self.product_id.product_tmpl_id.analytic_distribution:
            self.analytic_distribution = self.product_id.product_tmpl_id.analytic_distribution


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_analytic(self):
        if self.product_id and self.product_id.product_tmpl_id.analytic_distribution:
            self.analytic_distribution = self.product_id.product_tmpl_id.analytic_distribution


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_analytic(self):
        if self.product_id and self.product_id.product_tmpl_id.analytic_distribution:
            self.analytic_distribution = self.product_id.product_tmpl_id.analytic_distribution
