# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3),
        help='Date when the property is expected to be available',
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        default=2
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        string='State',
        selection=[('new', 'New'),
                   ('offer-received', 'Offer Received'),
                   ('offer-accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        default='new',
        copy=False
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        required=True,
    )

    # def action_create_estate_property(self):
    #     return {
    #         'name': ('Create Property'),
    #         'view_mode': 'list,form',
    #         'domain': [('estate_property', 'in', self.ids)],
    #         'res_model': 'estate.property',
    #         'type': 'ir.actions.act_window',
    #         'context': {'create': False, 'active_test': False},
    #     }
