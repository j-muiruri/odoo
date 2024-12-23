#define estate property offer model
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    
    price = fields.Float()
    status = fields.Selection(  selection=[('new', 'New'),
                   ('accepted', 'Accepted'),)
                   ('refused', 'Refused'),