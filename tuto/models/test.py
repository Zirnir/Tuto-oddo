from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test database"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90), 
        copy=False
    )
    
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(compute="_compute_price", readonly=True, store=False)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('south', 'South'), ('north', 'North'), ('east', 'East'), ('west', 'West')],
        help=""
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        default = 'new',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), 
                   ('canceled', 'Canceled')],
        help="",
        copy=False,
    )

    types = fields.Many2one("types", string="Property Type")
    agent = fields.Many2one("res.users", string="Real Estate Agent", default=lambda self: self.env.user)
    customer = fields.Many2one("res.partner", string="Buyer", copy=False, compute="_compute_buyer")

    tag = fields.Many2many("tag", string="Property Tag")

    offers = fields.One2many('offer', 'property', string="Offers")

    total_area = fields.Float(compute="_compute_total")

    best_offer = fields.Float(compute="_compute_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The price must be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The price must be positive')
    ]
    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(f"You cannot delete a property that is in state '{record.state}'.")
        return super(TestModel, self).unlink()

    @api.constrains('offers')
    def _check_offers(self):
        for record in self:
            if record.state == 'offer_accepted':
                accepted_offers = self.env['offer'].search([
                    ('property', '=', record.id),
                    ('status', '=', 'accepted')
                ])
                if not accepted_offers:
                    record.state = 'offer_received'

            elif record.state == 'offer_received':
                accepted_offers = self.env['offer'].search([
                    ('property', '=', record.id),
                    ('status', '=', 'accepted')
                ])
                if accepted_offers:
                    record.state = 'offer_accepted'

            elif record.state == 'new':
                offers_count = len(record.offers)
                if offers_count > 0:
                    record.state = 'offer_received'


    @api.onchange('garden')
    def _onchange_garden (self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    
    def _compute_offer(self):
        for record in self:
            offers = record.offers.mapped('price')
            if offers:
                record.best_offer = max(offers)
            else:
                record.best_offer = 0.0
            
    def solding(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Vous ne pouvez pas vendre une propriété annulée.")
            record.state = 'sold'
        return True
    
    def cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Vous ne pouvez pas annuler une propriété vendue.")
            record.state = 'canceled'
        return True
    
    @api.depends('offers.status', 'offers.price')
    def _compute_price(self):
        for record in self:
            accepted_offer = record.offers.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.selling_price = accepted_offer[0].price 
            else:
                record.selling_price = 0.0
    
    @api.depends('offers.status', 'offers.partner')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offers.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.customer = accepted_offer[0].partner.id  
            else:
                record.customer = False

