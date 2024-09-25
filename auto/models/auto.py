from odoo import fields, models, api
from datetime import date, timedelta

class Auto(models.Model):
    _name = "auto"
    _description = "Automobile"

    name = fields.Char(required=True)
    description = fields.Text()

    marque_id = fields.Many2one("marque", string="Auto Type",required=True)
    mod_id = fields.Many2one("mod", string="Auto Model",required=True, domain="[('marque_id', '=', marque_id)]")

    type_id = fields.Many2one("type", string="Auto Type",required=True)
    carbuant = fields.Selection(required=True,
    selection=[('diessel', 'Diessel'), ('essence', 'Essence'), ('electrique', 'Electrique')],
    )

    price = fields.Integer(required=True)

    option = fields.Boolean(default=False)

    option_ids = fields.Many2many("option", String="Options", domain="[('mod_id', '=', mod_id)]")

    img = fields.Image(string="Photo", max_width=384, max_height=384)