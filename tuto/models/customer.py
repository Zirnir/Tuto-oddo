from odoo import fields, models

class Customer(models.Model):
    _name = "customer"
    _description = "Customer of Property"

    name = fields.Char()