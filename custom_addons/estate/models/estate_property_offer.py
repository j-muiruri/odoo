# define estate property offer model
from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    
    @api.constrains('price')
    def _check_offer_price(self):
        for offer in self:
            if offer.price <= 0:
                raise ValidationError(
                    'The offer price must be strictly positive')

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
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            # get difference between deadline date and today
            date_format = "%Y-%m-%d"

            # convert string date to datetime object and calculate difference in days between them
            d1 = datetime.strptime(
                offer.date_deadline.strftime(date_format), date_format)
            d2 = datetime.strptime(
                fields.Date.today().strftime(date_format), date_format)
            diff = d1 - d2

            # calculate validity in days
            offer.validity = abs(diff.days)

    @api.constrains('status', 'property_id')
    def _check_offer_status_per_parent(self):
        for record in self:
            if record.status == 'accepted':  # only check if any offer is accepted for a parent
                existing_records = self.search([
                    ('status', '=', 'accepted'),
                    ('property_id', '=', record.property_id.id),
                    ('id', '!=', record.id)  # exclude the current record
                ])
                if existing_records:
                    raise ValidationError(
                        "An accepted offer already exists for the current property" % record.property_id)

    def write(self, vals):
        # Check before writing if the value is being updated
        if 'status' in vals and vals['status'] == 'accepted':
            existing_records = self.search([
                ('status', '=', vals['status']),
                ('property_id', '=', self.property_id.id),
                ('id', '!=', self.id)
            ])
            if existing_records:
                raise ValidationError(
                    "An accepted offer already exists for the current property" % self.property_id)
        return super(EstatePropertyOffer, self).write(vals)

    def action_accept_offer(self):
        for offer in self:
            # set the status to accepted and update the selling price and buyer details.
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id.id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = 0.00
            offer.property_id.buyer_id = ''

        return True
    
    