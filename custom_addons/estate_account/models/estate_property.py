# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        # print("This is a test")
        return super(EstateProperty, self).action_sell_property()
