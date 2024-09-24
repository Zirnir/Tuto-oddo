from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError,ValidationError

class Offer(models.Model):
    _name = "offer"
    _description = "Offers for property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Status of the offer",
        copy=False
    )
    partner = fields.Many2one('res.partner', string="Partner", required=True)
    property = fields.Many2one('test.model', string="Property")
    types = fields.Many2one("types", string="Property Type", compute="_compute_type")
    

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity")
    create_date = fields.Date(default=lambda self: date.today())

    property_type_id = fields.Many2one(related="property.types", store=True, string="Type Property")

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The price must be positive')
        
    ]

    @api.model
    def create(self, vals):
        existing_offers = self.search([
            ('property', '=', vals.get('property')),
        ])
        for offer in existing_offers:
            if vals['price'] < offer.price:
                raise ValidationError("Cannot create this offer. The amount must be greater than existing offers.")
        
        return super(Offer, self).create(vals)
                    
    @api.constrains('status')
    def _check_unique_accepted(self):
        for record in self:
            if record.status == 'accepted':
                accepted_offers = self.search([
                    ('property', '=', record.property.id),
                    ('status', '=', 'accepted'),
                    ('id', '!=', record.id)
                ])
                if accepted_offers:
                    record.status = 'refused'    

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _compute_type(self):
        for record in self:
            record.types = record.property_type_id

    def _inverse_validity(self):
        for record in self:
                record.validity = (record.date_deadline - record.create_date).days

    def accepted(self):
        for record in self:
            valid_sell_price = (record.property.expected_price/10)*9
            if record.price >= valid_sell_price:
                record.status = 'accepted'
                record.property.state = 'offer_accepted'
            else:
                raise UserError(f"L'offre doit être aux minimum à {valid_sell_price}.")
    
    def refused(self):
        for record in self:
            record.status = 'refused'
            if record.property.state != 'sold':
                if record.property.state != 'offer_accepted':
                    record.property.state = 'offer_received'
    
