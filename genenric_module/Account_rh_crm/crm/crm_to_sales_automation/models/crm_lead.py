# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ready_for_order = fields.Boolean(string="Ready for Order", default=False)
    sale_order_id = fields.Many2one('sale.order', string="Related Sale Order", readonly=True)
    lead_product_line_ids = fields.One2many('crm.lead.product.line', 'lead_id', string="Primarily Interested Products")

    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase Orders', compute='_compute_purchase_orders', store=True)
    purchase_order_count = fields.Integer(compute='_compute_purchase_orders', store=False)

    stock_status = fields.Selection([
        ('sufficient', 'Stock Sufficient'),
        ('restock_needed', 'Restock Needed'),
        ('purchase_order_created', 'Purchase Order Created'),
        ('unknown', 'Unknown')
    ], string="Stock Status", compute="_compute_stock_status", store=True)

    stock_check_count = fields.Integer(string="Products Needing Restock", compute="_compute_stock_status", store=True)

    order_created = fields.Boolean(
        string="Order Created",
        compute='_compute_order_created',
        store=True,
    )
    stock_needed = fields.Boolean(
        string="Stock Needed",
        compute='_compute_stock_needed',
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        # _logger.info("CREATE CALLED on crm.lead with vals: %s", vals_list)
        leads = super().create(vals_list)
        for lead in leads:
            if lead.ready_for_order and not lead.sale_order_id and lead.partner_id:
                order = self.env['sale.order'].create({
                    'partner_id': lead.partner_id.id,
                    'origin': f"Lead: {lead.name}",
                    'note': f"Auto-created from CRM Lead"
                })
                for product_line in lead.lead_product_line_ids:
                    self.env['sale.order.line'].create({
                        'order_id': order.id,
                        'product_id': product_line.product_id.id,
                        'product_uom_qty': product_line.quantity,
                        'price_unit': product_line.product_id.list_price,
                        'name': "Auto-added from lead",
                        'auto_generated': True,
                    })
                lead.sale_order_id = order.id
        return leads

    def write(self, vals):
        # _logger.info("WRITE CALLED on crm.lead with vals: %s", vals)
        result = super().write(vals)
        for lead in self:
            # Only trigger when the checkbox is checked
            if vals.get('ready_for_order') and not lead.sale_order_id and lead.partner_id:
                order = self.env['sale.order'].create({
                    'partner_id': lead.partner_id.id,
                    'origin': f"Lead: {lead.name}",
                    'note': f"Auto-generated from CRM Lead: {lead.name}"
                })
                for product_line in lead.lead_product_line_ids:
                    self.env['sale.order.line'].create({
                        'order_id': order.id,
                        'product_id': product_line.product_id.id,
                        'product_uom_qty': product_line.quantity,
                        'price_unit': product_line.product_id.list_price,
                        'name': "Auto-added from lead",
                        'auto_generated': True,
                    })
                lead.sale_order_id = order.id
        return result

    @api.depends('sale_order_id')
    def _compute_purchase_orders(self):
        for lead in self:
            po_ids = self.env['purchase.order'].search([('origin', 'ilike', lead.sale_order_id.name)])
            lead.purchase_order_ids = po_ids
            lead.purchase_order_count = len(po_ids)

    def action_open_sale_order(self):
        # _logger.info("\n\nReturning action for SO ID: %s\n", self.sale_order_id.id)
        self.ensure_one()
        if self.sale_order_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale Order',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': self.sale_order_id.id,
            }

    def action_view_purchase_orders(self):
        # _logger.info("\n\nReturning action for SO ID: %s\n", self.purchase_order_ids.ids)
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.purchase_order_ids.ids)]
        }

    def action_view_desired_products(self):
        self.ensure_one()
        # Base domain: all lines for this lead
        domain = [('lead_id', '=', self.id)]
        # If restock is needed, narrow it down to only those lines where qty > available
        if self.stock_status == 'restock_needed':
            lines_needing = self.lead_product_line_ids.filtered(
                lambda l: l.quantity > l.product_id.qty_available
            )
            domain = [('id', 'in', lines_needing.ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Primarily Interested Products',
            'view_mode': 'list,form',
            'res_model': 'crm.lead.product.line',
            'domain': domain,
            'context': {'default_lead_id': self.id},
        }

    @api.depends('sale_order_id', 'sale_order_id.order_line', 'sale_order_id.order_line.product_id.qty_available', 'purchase_order_ids', 'lead_product_line_ids', 'lead_product_line_ids.product_id.qty_available')
    def _compute_stock_status(self):
        for lead in self:
            # Priority 1: If purchase order exists
            if  lead.sale_order_id and lead.purchase_order_ids:
                lead.stock_status = 'purchase_order_created'
                lead.stock_check_count = 0
                continue

            # Priority 2: If a sale order exists, check its lines
            elif lead.sale_order_id and lead.sale_order_id.order_line:
                restock_count = 0
                for line in lead.sale_order_id.order_line:
                    if line.product_id.qty_available < line.product_uom_qty:
                        restock_count += 1
                lead.stock_check_count = restock_count
                lead.stock_status = 'restock_needed' if restock_count else 'sufficient'
                continue

            # Priority 3: Fallback to lead product lines
            elif lead.lead_product_line_ids:
                restock_count = 0
                for line in lead.lead_product_line_ids:
                    if line.quantity > line.product_id.qty_available:
                        restock_count += 1
                lead.stock_check_count = restock_count
                lead.stock_status = 'restock_needed' if restock_count else 'sufficient'
                continue

            # Default: No information
            lead.stock_status = 'unknown'
            lead.stock_check_count = 0
    
    @api.depends('sale_order_id', 'purchase_order_ids')
    def _compute_order_created(self):
        for lead in self:
            lead.order_created = bool(lead.sale_order_id)

    @api.depends('purchase_order_ids')
    def _compute_stock_needed(self):
        for lead in self:
            lead.stock_needed = bool(lead.purchase_order_ids)