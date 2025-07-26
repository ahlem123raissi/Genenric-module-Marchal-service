# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    advance_payment_account_id = fields.Many2one('account.account', domain="[('account_type','in',['liability_current'])]", string="Advance Payment Account")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    advance_payment_account_id = fields.Many2one('account.account', related='company_id.advance_payment_account_id', readonly=False)