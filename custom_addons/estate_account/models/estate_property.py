# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime;


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        # print("This is a test")
        # if math.isclose(self.selling_price,  0.00):
        
        if self.selling_price == False or self.selling_price is None:
            raise UserError("Selling price cannot be zero")
        
        records = []
        invoice = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'name': 'EPRP/' + datetime.datetime.now().strftime('%Y') + str(self.id),
            'amount_total': self.selling_price,
            'date': fields.Date.today(),
            'invoice_line_ids': [
                fields.Command.create({
                    'name': 'Property Sales',
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                fields.Command.create({
                    'name': 'Sales Tax',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price + 100,
                }),
            ],
        }

        records.append(invoice)
        self.env['account.move'].create(records)

        return super(EstateProperty, self).action_sell_property()
