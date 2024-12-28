# define estate property offer model
from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta
from datetime import datetime,date,timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
    )
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            #get difference between deadline date and today
            date_format = "%Y-%m-%d";
            
            # convert string date to datetime object and calculate difference in days between them
            d1 = datetime.strptime(offer.date_deadline.strftime(date_format), date_format)
            d2 = datetime.strptime(fields.Date.today().strftime(date_format), date_format)
            diff = d1 - d2
            
            # calculate validity in days
            offer.validity = abs(diff.days)
            
    def action_accept_offer(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id.id
        return True
    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True