# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _inherit = ['mail.thread',
        'mail.activity.mixin']
    _description = "Advance Payment"

    name = fields.Char('Advance Payment', required=True, default="NEW")
    payment_type = fields.Selection([('customer','Customer'),('supplier','Supplier')], string="Payment Type", default="customer", tracking=True)
    partner_id = fields.Many2one('res.partner', 'Partner', tracking=True, )
    journal_id = fields.Many2one('account.journal', tracking=True, domain="[('type','in',['sale'])]")
    currency_id = fields.Many2one('res.currency','Currency')
    amount = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([('draft','Draft'),('confirm','Confirm')], default='draft', tracking=True)
    move_ids = fields.Many2many('account.move', 'rel_account_move_advance_payment', 'move_id','advance_payment_id', copy=False)
    company_id = fields.Many2one('res.company', default= lambda self:self.env.company.id)
    count_moves = fields.Integer('Count Moves', compute="_compute_count_moves")
    tax_ids = fields.Many2many('account.tax','rel_advance_payment_account_tax','advance_payment_id','tax_ids', string="Taxes")
    is_reconciled = fields.Boolean('Is Reconciled', copy=False)
    amount_incl_tax = fields.Monetary(currency_field='currency_id', compute="compute_amount_incl_tax", store=True, string="Amount (Inc Tax)")

    @api.depends('amount','tax_ids')
    def compute_amount_incl_tax(self):
        for record in self:
            amount_incl_tax = record.amount
            if record.tax_ids and record.amount:
                for tax_id in record.tax_ids:
                    amount_incl_tax += record.amount * (tax_id.amount/100)
            record.amount_incl_tax = amount_incl_tax



    # @api.depends('move_ids','state')
    # def _compute_is_reconciled(self):
    #     for record in self:
    #         move_id = record.move_ids.mapped('line_ids').filtered(
    #                 lambda x: x.account_type
    #                 in ("asset_receivable", "liability_payable")
    #                 and not x.reconciled
    #             )
    #         if move_id or record.state == 'draft':
    #             record.is_reconciled = False
    #         else:
    #             record.is_reconciled = True


    @api.depends('move_ids','state')
    def _compute_count_moves(self):
        for record in self:
            record.count_moves = len(record.move_ids)
        
    
    @api.onchange('journal_id')
    def onchange_journal_id(self):
        for record in self:
            record.currency_id = record.journal_id.currency_id.id if record.journal_id.currency_id else record.company_id.currency_id.id

    @api.model
    def create_advance_payment_sequences(self):
        # Define the sequence for Customer Advance Payments
        customer_sequence = self.env['ir.sequence'].search([('code','=','ADV.CUST'),('company_id','=',self.company_id.id)], limit=1)

        if not customer_sequence:
            customer_sequence = self.env['ir.sequence'].create({
                'name': 'Customer Advance Payment',
                'code': 'ADV.CUST',
                'prefix': 'ADV-CUST-%(year)s-%(month)s-',
                'padding': 3,
                'implementation': 'no_gap',  # No gaps in sequence
                'number_next': 1,
                'active': True,
                'company_id':self.company_id.id,
            })
        supplier_sequence = self.env['ir.sequence'].search([('code','=','ADV.SUPP'),('company_id','=',self.company_id.id)], limit=1)
        if not supplier_sequence:

            # Define the sequence for Supplier Advance Payments
            supplier_sequence = self.env['ir.sequence'].create({
                'name': 'Supplier Advance Payment',
                'code': 'ADV.SUPP',
                'prefix': 'ADV-SUPP-%(year)s-%(month)s-',
                'padding': 3,
                'implementation': 'no_gap',  # No gaps in sequence
                'number_next': 1,
                'active': True,
                'company_id':self.company_id.id,
            })

        return customer_sequence if self.payment_type == 'customer' else supplier_sequence
    
    @api.model
    def create(self, vals):
        result = super().create(vals)
        for record in result:
            sequence = record.create_advance_payment_sequences().next_by_id()
            record.name = sequence
        return result

    def _action_create_first_move(self):
        first_move_vals = {
            'move_type':'out_invoice',
            'ref':self.name,
            'journal_id':self.journal_id.id,
            'partner_id':self.partner_id.id,
            'currency_id':self.currency_id.id,
            'date':fields.Date.today()
        }
        if self.payment_type == 'customer':
            
            advance_payment_account_id = self.company_id.advance_payment_account_id
            if not advance_payment_account_id:
                raise UserError(_("Please configure Advance Payment Account in Settings.."))
            # first_line_vals = [{
            #     'name':'ADVANCE PAYMENT : '+self.name,
            #     'account_id':advance_payment_account_id.id,
            #     'credit':self.amount_incl_tax,
            #     'partner_id':self.partner_id.id,
            #     },
            #     {
            #     'name':'ADVANCE PAYMENT : '+self.name,
            #     'account_id':self.journal_id.default_account_id.id,
            #     'debit':self.amount_incl_tax,
            #     'partner_id':self.partner_id.id,
            #     }
            #     ]

            first_line_vals = [{
                'account_id':advance_payment_account_id.id,
                'name':'ADVANCE PAYMENT : '+self.name,
                'partner_id':self.partner_id.id,
                'quantity':1,
                'price_unit':self.amount,
                'tax_ids':[(6,0,self.tax_ids.ids)]
            }]
            # credit
            
        else:
            # first_move_vals['move_type'] = 'in_invoice'
            first_line_vals = [{
                'name':'ADVANCE PAYMENT : '+self.name,
                'account_id':self.property_account_income_id.id,
                'quantity':1,
                'price_unit':self.amount,
                'tax_ids':[(6,0,self.tax_ids.ids)],
            }]
        first_move_vals.update({
            'invoice_line_ids':[(0,0, first_line_val) for first_line_val in first_line_vals]
        })
        first_move_id = self.env['account.move'].create(first_move_vals)
        self.move_ids = [(4,first_move_id.id)]

    def _action_create_second_move(self):
        second_move_vals = {
            'move_type':'entry',
            'ref':self.name,
            'journal_id':self.journal_id.id,
            'partner_id':self.partner_id.id,
            'currency_id':self.currency_id.id,
            'date':fields.Date.today()
        }
        if self.payment_type == 'customer':
            receivable_account_id = self.partner_id.property_account_receivable_id
            if not receivable_account_id:
                receivable_account_id = self.env['account.account'].search([('account_type','=','asset_receivable'),('reconcile','=',True)], limit=1)
            if not receivable_account_id:
                raise UserError(_("Account Not Found \n Type : Receivable"))
            advance_payment_account_id = self.company_id.advance_payment_account_id
            if not advance_payment_account_id:
                raise UserError(_("Please configure Advance Payment Account in Settings.."))
            
            second_line_vals = [
            # credit val    
            {
                'credit':self.amount_incl_tax,
                'account_id':receivable_account_id.id,
                'name':self.name,
                'partner_id':self.partner_id.id,
            },
            # debit val
            {
                'debit':self.amount_incl_tax,
                'account_id':advance_payment_account_id.id,
                'name':self.name,
                'partner_id':self.partner_id.id,
            },
            ]
        else:
            payable_account_id = self.env.ref('account.1_payable')
            if not payable_account_id:
                payable_account_id = self.env['account.account'].search([('account_type','=','liability_payable'),('reconcile','=',True)], limit=1)
            if not payable_account_id:
                raise UserError(_("Account Not Found \n Type : Payable"))
            second_line_vals = [
            # credit val    
            {
                'credit':self.amount,
                'account_id':self.asset_account_id.id,
                'name':self.name,
                'partner_id':self.partner_id.id,
            },
            # debit val
            {
                'debit':self.amount,
                'account_id':payable_account_id.id,
                'name':self.name,
                'partner_id':self.partner_id.id,
            },
            ]
        second_move_vals.update({
            'line_ids':[(0,0, second_line_val) for second_line_val in second_line_vals]
        })
        second_move_id = self.env['account.move'].create(second_move_vals)
        self.move_ids = [(4,second_move_id.id)]


    def action_confirm(self):
        for payment in self:
            payment.onchange_journal_id()
            payment._action_create_first_move()
            # payment._action_create_second_move()
            for move_id in payment.move_ids:
                move_id.action_post()
        self.update({
            'state':'confirm',
        })
    
    def action_view_entries(self):
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
        context = eval(action.get('context')) if action.get('context') else {}
        context.update({
            'create':False,
        })
        action['context'] = context
        action['domain'] = [('id','in',self.move_ids.ids)]
        return action
        
                

