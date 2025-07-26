# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError
from odoo import api, fields


@tagged('test_advance_payment')
class TestPurchaseAdvancePayment(TransactionCase):
    """
    Tests for advance payments on purchase orders.
    Checks:
    - Down payment by percentage
    - Down payment by fixed amount
    Verifies vendor bill creation and correct behavior.
    """

    def setUp(self):
        super().setUp()

        # Create test product
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0
        })

        # Create down payment product and config param
        self.dp_product = self.env['product.product'].create({
            'name': 'Advance Payment Product',
            'type': 'service',
            'list_price': 0.0,
        })

        # set the Advance Payment Product
        self.env['ir.config_parameter'].sudo().set_param(
            'purchase.advance_payment_product_id',
            self.dp_product.id
        )

        # Create partner
        self.partner = self.env['res.partner'].create({
            'name': 'Vendor Test',
            'supplier_rank': 1,
        })

        # Create purchase order
        self.po = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'name': self.product.name,
                'product_qty': 1,
                'price_unit': 100.0,
                'date_planned': fields.Datetime.now(),
            })]
        })
        self.po.button_confirm()

    def test_down_payment_by_percentage(self):
        """
        Test vendor bill creation using percentage-based down payment.
        Ensures the wizard returns a valid action, creates a draft bill,
        and sets correct origin and amount.
        """
        wizard = self.env['purchase.advance.payment.inv'].with_context(active_ids=[self.po.id]).create({
            'advance_payment_method': 'percentage',
            'amount': 100.0,
            'purchase_order_id': self.po.id,
        })
        result = wizard.create_vander_bills_action_btn()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('res_model'), 'account.move')

        bill = self.env['account.move'].browse(result['res_id'])
        self.assertTrue(bill.exists(), "Vendor bill was not created.")
        self.assertEqual(bill.invoice_origin, self.po.name)
        self.assertEqual(bill.state, 'draft')
        self.assertEqual(bill.amount_total, 100.0)

    def test_down_payment_by_fixed_amount(self):
        """
        Test vendor bill creation using Fixed Amount based down payment.
        Ensures the wizard returns a valid action, creates a draft bill,
        and sets correct origin and amount.
        """
        wizard = self.env['purchase.advance.payment.inv'].with_context(active_ids=[self.po.id]).create({
            'advance_payment_method': 'fixed',
            'fixed_amount': 100.0,
            'purchase_order_id': self.po.id,
        })
        result = wizard.create_vander_bills_action_btn()
        bill = self.env['account.move'].browse(result['res_id'])
        self.assertEqual(len(bill.invoice_line_ids), 1)
        self.assertAlmostEqual(bill.amount_total, 100.0, places=2)

    def test_down_payment_above_due_should_raise(self):
        """
        Test that a UserError is raised when trying to create a vendor bill
        with a down payment percentage that exceeds the remaining amount due
        on the purchase order.

        The wizard should prevent creating a bill if the calculated down payment
        amount (based on percentage) is greater than the remaining amount of the PO.
        """

        po = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'name': self.product.name,
                'product_qty': 1,
                'price_unit': 100.0,
            })],
        })
        po.button_confirm()

        # Create full invoice and post it
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': po.partner_id.id,
            'invoice_origin': po.name,
            'invoice_date': fields.Datetime.now(),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'name': self.product.name,
                'quantity': 1,
                'price_unit': 100.0,
            })],
        })
        bill.action_post()

        # Fully invoice PO first
        self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.po.partner_id.id,
            'invoice_origin': self.po.name,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'name': self.product.name,
                'quantity': 1,
                'price_unit': 100.0,
            })]
        })
        wizard = self.env['purchase.advance.payment.inv'].with_context(active_ids=[self.po.id]).create({
            'advance_payment_method': 'fixed',
            'fixed_amount': 100.0,
            'purchase_order_id': po.id,
        })

        with self.assertRaises(UserError):
            wizard.create_vander_bills_action_btn()
