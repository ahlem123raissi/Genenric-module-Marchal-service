# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2024 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import fields, models,api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    inventory_zone_id = fields.Many2one('stock.inventory.zone',
                                        string='Inventory Zone',
                                        help="Inventory location zones")


    @api.onchange('inventory_zone_id')
    def _onchange_inventory_zone_id(self):
        if self.inventory_zone_id:
            location = self.env["stock.location"].search([('inventory_zone_id','=',self.inventory_zone_id.id)])
            if location:
                self.location_id = location[0].id
            else:
                self.location_id = False

    @api.model
    def _get_inventory_fields_write(self):
        fields = super(StockQuant, self)._get_inventory_fields_write()
        fields = fields + ['inventory_zone_id']
        return fields
