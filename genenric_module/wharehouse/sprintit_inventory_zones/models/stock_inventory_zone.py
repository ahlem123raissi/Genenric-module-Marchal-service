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


class StockInventoryZone(models.Model):
    _name = 'stock.inventory.zone'

    name = fields.Char('Inventory Zone', help="Inventory location zones")
