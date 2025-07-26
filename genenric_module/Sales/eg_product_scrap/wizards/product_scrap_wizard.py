from odoo import fields, models, api


class ProductScrapWizard(models.TransientModel):
    _name = "product.scrap.wizard"
    _description = "Product Scrap"

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    location_id = fields.Many2one(comodel_name="stock.location", string="Location")
    qty_available = fields.Float(string="Available Quantity")
    scrap_qty = fields.Float(string="Scrap")
    scrap_location_id = fields.Many2one(comodel_name="stock.location", string="Scrap Location")

    @api.model
    def default_get(self, fields_list):
        res = super(ProductScrapWizard, self).default_get(fields_list)
        product_id = self.env["product.product"].browse(self._context.get("active_id"))
        quant_ids = self.env["stock.quant"].search([("product_id", "=", product_id.id), ("on_hand", "=", True)])
        res["product_id"] = product_id.id
        res["qty_available"] = 0 if len(quant_ids) > 1 else quant_ids.available_quantity
        if len(quant_ids) == 1:
            res["location_id"] = quant_ids.location_id.id
        return res

    def scrap_product(self):
        scrap_id = self.env["stock.scrap"].create({
            "name": self.env['ir.sequence'].next_by_code('stock.scrap') or _('New'),
            "product_id": self.product_id.id,
            "product_uom_id":self.product_id.uom_id.id,
            "scrap_qty": self.scrap_qty,
            'location_id': self.location_id.id,
            'scrap_location_id': self.scrap_location_id.id,
        })
        move_id = self.env['stock.move'].create({
            'name': self.product_id.name,
            'origin': None,
            'company_id': self.env.user.company_id.id,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'state': 'draft',
            'product_uom_qty': self.scrap_qty,
            'location_id': self.location_id.id,
            'scrapped': True,
            'location_dest_id': self.scrap_location_id.id,
            'move_line_ids': [(0, 0, {'product_id': self.product_id.id,
                                      'product_uom_id': self.product_id.uom_id.id,
                                      'quantity': self.scrap_qty,
                                      'location_id': self.location_id.id,
                                      'location_dest_id': self.scrap_location_id.id
                                      })],
            #             'restrict_partner_id': self.owner_id.id,
        })
        move_id.with_context(is_scrap=True)._action_done()
        scrap_id.write({'move_ids': move_id.ids, 'state': 'done'})
        scrap_id.date_done = fields.Datetime.now()
