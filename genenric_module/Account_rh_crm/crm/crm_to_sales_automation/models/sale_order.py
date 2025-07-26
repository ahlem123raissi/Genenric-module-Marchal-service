# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lead_ids = fields.One2many('crm.lead', 'sale_order_id', string="Related Lead/Opportunity")

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for line in order.order_line:
                product = line.product_id
                required_qty = line.product_uom_qty
                available_qty = product.qty_available

                if available_qty < required_qty:
                    if not product.seller_ids:
                        raise UserError(f"No vendor found for product '{product.display_name}'. Cannot auto-create Purchase Order.")

                    vendor = product.seller_ids[0].partner_id.id

                    needed_qty = required_qty - available_qty

                    purchase_order = self.env['purchase.order'].create({
                        'partner_id': vendor,
                        'origin': f"Restock for {order.name}",
                        'order_line': [(0, 0, {
                            'product_id': product.id,
                            'name': product.name or product.display_name,
                            'product_qty': needed_qty,
                            'product_uom': product.uom_po_id.id,
                            'price_unit': product.standard_price,
                            'date_planned': fields.Date.today(),
                        })],
                    })

                    lead = self.env['crm.lead'].search([('sale_order_id', '=', order.id)], limit=1)
                    if lead:
                        lead.message_post(
                            subject="Auto-generated Purchase Order",
                            body=f"""Stock Alert: Insufficient stock for {product.name}. Purchase Order {purchase_order.id} created.""",
                            message_type='comment',
                            subtype_id=self.env.ref('mail.mt_note').id
                        )
        return res


# from odoo.exceptions import UserError
# from odoo.fields import Date

# def action_confirm(self):
#     res = super().action_confirm()

#     for order in self:
#         for line in order.order_line:
#             product = line.product_id
#             required_qty = line.product_uom_qty
#             available_qty = product.qty_available

#             if available_qty < required_qty:
#                 needed_qty = required_qty - available_qty

#                 # Use Odoo's smart vendor selection
#                 seller = product._select_seller(
#                     quantity=needed_qty,
#                     uom=product.uom_po_id,
#                     date=Date.today(),
#                     partner=None  # You could pass a specific vendor if needed
#                 )

#                 if not seller:
#                     raise UserError(f"No suitable vendor found for product '{product.display_name}'.")

#                 purchase_order = self.env['purchase.order'].create({
#                     'partner_id': seller.partner_id.id,
#                     'origin': f"Restock for {order.name}",
#                     'order_line': [(0, 0, {
#                         'product_id': product.id,
#                         'name': product.name or product.display_name,
#                         'product_qty': needed_qty,
#                         'product_uom': product.uom_po_id.id,
#                         'price_unit': seller.price or product.standard_price,
#                         'date_planned': Date.today(),
#                     })],
#                 })

#                 # Link to lead and log message
#                 lead = self.env['crm.lead'].search([('sale_order_id', '=', order.id)], limit=1)
#                 if lead:
#                     lead.message_post(body=(
#                         f"⚠️ Stock insufficient for <b>{product.name}</b>. "
#                         f"Purchase Order <b>{purchase_order.name}</b> created."
#                     ))

#     return res