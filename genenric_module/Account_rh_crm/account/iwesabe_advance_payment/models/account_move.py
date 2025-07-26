# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_add_advance_payment(self):
        for record in self.filtered(lambda x:x.move_type == 'out_invoice'):
            payment_id = self.env['advance.payment'].search([('is_reconciled','=',False),('partner_id','=',record.partner_id.id),('state','=','confirm')], limit=1)
            advance_payment_account_id = self.company_id.advance_payment_account_id
            if payment_id:
                record.invoice_line_ids = [(0,0, {
                'account_id':advance_payment_account_id.id,
                'name':f'ADVANCE PAYMENT (ref : {payment_id.name})',
                # 'partner_id':self.partner_id.id,
                'quantity':-1,
                'price_unit':payment_id.amount,
                'tax_ids':[(6,0,payment_id.tax_ids.ids)],
                'adv_payment_id':payment_id.id
                 })]
                payment_id.is_reconciled = True
            else:
                raise UserError(_("ADVANCE PAYMENT NOT FOUND..."))



    # def action_post(self):
    #     result = super().action_post()
    #     for record in self:
    #         record._action_reconcile_advance_pymt()
    #     return result

    def _action_reconcile_advance_pymt(self):
        if self.move_type == "out_invoice":
            payment_ids = (
                self.env["advance.payment"]
                .search(
                    [
                        # ("is_advance_payment", "=", True),
                        ("payment_type", "=", "customer"),
                        ("partner_id", "=", self.partner_id.id),
                        ("state", "=", "confirm"),
                    ]
                )
                .filtered(lambda x: not x.is_reconciled)
            )
            if payment_ids:
                line_ids = payment_ids.mapped("move_ids.line_ids").filtered(
                    lambda x: x.account_type
                    in ("asset_receivable", "liability_payable")
                    and not x.reconciled
                )
                if line_ids:
                    reconcile_line = self.line_ids.filtered(
                        lambda x: x.account_type
                        in ("asset_receivable", "liability_payable")
                        and not x.reconciled
                    )
                    if reconcile_line:
                        line_ids += reconcile_line
                        line_ids.reconcile()
        elif self.move_type == "in_invoice":
            payment_ids = (
                self.env["advance.payment"]
                .search(
                    [
                        # ("is_advance_payment", "=", True),
                        ("payment_type", "=", "supplier"),
                        # ("partner_type", "=", "supplier"),
                        ("partner_id", "=", self.partner_id.id),
                        ("state", "=", "confirm"),
                    ]
                )
                .filtered(lambda x: not x.is_reconciled)
            )
            if payment_ids:
                line_ids = payment_ids.mapped("move_ids.line_ids").filtered(
                    lambda x: x.account_type
                    in ("asset_receivable", "liability_payable")
                    and not x.reconciled
                )
                if line_ids:
                    reconcile_line = self.line_ids.filtered(
                        lambda x: x.account_type
                        in ("asset_receivable", "liability_payable")
                        and not x.reconciled
                    )
                    if reconcile_line:
                        line_ids += reconcile_line
                        line_ids.reconcile()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    adv_payment_id = fields.Many2one('advance.payment', copy=False)

    def unlink(self):
        for record in self:
            if record.adv_payment_id:
                record.adv_payment_id.is_reconciled = False
        return super().unlink()
