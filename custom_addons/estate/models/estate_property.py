# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta

from odoo.exceptions import UserError, ValidationError


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

    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user.id
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tag',
        required=True,
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        copy=False,
    )
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            # property.best_price = max(offer.price for offer in property.offer_ids)
            property.best_price = max(property.offer_ids.mapped('price')) if property.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
            self.garden_area = 10 if self.garden else 0
            self.garden_orientation = 'north' if self.garden else False
            
    def action_sell_property(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold") 
            else:
                property.state = 'sold'
        
    def action_cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold property cannot be canceled") 
            else:
                property.state = 'cancelled'
    
