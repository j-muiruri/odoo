# define estate.property.type model
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _check_unique_name = models.Constraint(
        'unique(name)', 'Name must be unique')
    _order = 'sequence'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer(
        string='Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')
    
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)