# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2024 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    inventory_zone_id = fields.Many2one('stock.inventory.zone',
                                        string='Inventory Zone', index=True,
                                        help="Inventory location zones")
