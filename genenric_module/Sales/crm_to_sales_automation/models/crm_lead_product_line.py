# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CrmLeadProductLine(models.Model):
    _name = 'crm.lead.product.line'
    _description = 'Lead Product Line'

    lead_id = fields.Many2one('crm.lead', string="Lead", ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    list_price = fields.Float(string="Unit price", related='product_id.list_price')

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            lead = record.lead_id
            if lead.ready_for_order and lead.sale_order_id:
                # Optional: Remove old auto-generated lines first
                lead.sale_order_id.order_line.filtered(lambda l: l.auto_generated).unlink()

                for product_line in lead.lead_product_line_ids:
                    record.env['sale.order.line'].create({
                        'order_id': lead.sale_order_id.id,
                        'product_id': product_line.product_id.id,
                        'product_uom_qty': product_line.quantity,
                        'price_unit': product_line.product_id.list_price,
                        'name': "Auto-updated from lead",
                        'auto_generated': True
                    })
        return records

    def write(self, vals):
        res = super().write(vals)

        leads_to_update = self.mapped('lead_id').filtered(lambda l: l.ready_for_order and l.sale_order_id)

        for lead in leads_to_update:
            # Remove old auto-generated lines
            lead.sale_order_id.order_line.filtered(lambda l: l.auto_generated).unlink()

            # Add updated lines from lead
            for product_line in lead.lead_product_line_ids:
                self.env['sale.order.line'].create({
                    'order_id': lead.sale_order_id.id,
                    'product_id': product_line.product_id.id,
                    'product_uom_qty': product_line.quantity,
                    'price_unit': product_line.product_id.list_price,
                    'name': "Auto-updated from lead",
                    'auto_generated': True,
                })
        return res
        
    def unlink(self):
        leads_to_update = self.mapped('lead_id').filtered(lambda l: l.ready_for_order and l.sale_order_id)
        res = super().unlink()
        for lead in leads_to_update:
            # Remove all old lines
            lead.sale_order_id.order_line.filtered(lambda l: l.auto_generated).unlink()

            for product_line in lead.lead_product_line_ids:
                self.env['sale.order.line'].create({
                    'order_id': lead.sale_order_id.id,
                    'product_id': product_line.product_id.id,
                    'product_uom_qty': product_line.quantity,
                    'price_unit': product_line.product_id.list_price,
                    'name': "Auto-updated from lead",
                    'auto_generated': True
                })
        return res