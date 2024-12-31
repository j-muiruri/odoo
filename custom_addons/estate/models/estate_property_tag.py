# define estate.property.tag model
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _check_unique_name = models.Constraint('unique(name)', 'Name must be unique')
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

