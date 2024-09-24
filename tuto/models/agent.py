from odoo import fields, models

class Agent(models.Model):
    _name = "agent"
    _description = "Agent sold the property"

    name = fields.Char(required=True)