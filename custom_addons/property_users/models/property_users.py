# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PropertyUsers(models.Model):
    # _name = 'property.users'
    _inherit = 'res.users'
    property_ids = fields.Many2one(
        'estate.property',
        string='Properties',
        domain="[('state', 'in', ['new','offer-received'])]")
