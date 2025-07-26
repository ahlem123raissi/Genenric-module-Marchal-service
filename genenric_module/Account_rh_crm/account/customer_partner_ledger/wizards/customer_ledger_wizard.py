from odoo import models, fields, api

class CustomerLedgerWizard(models.TransientModel):
    _name = 'customer.ledger.wizard'
    _description = 'Customer Ledger Wizard'

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)

    def action_generate_ledger(self):
        """
        Triggers the QWeb PDF report for the customer ledger.
        """
        self.ensure_one()

        return self.env.ref('customer_partner_ledger.customer_ledger_report').report_action(
            self.env['customer.ledger.report'].create({'customer_id': self.customer_id.id})
        )
