from odoo import fields, models

class Marque(models.Model):
    _name = "marque"
    _description = "Marque of Auto"

    name = fields.Char(required=True)
    logo = fields.Image(string="Logo", max_width=128, max_height=128)

    auto_ids = fields.One2many('auto', 'marque_id', string="Auto", readonly=True)
    mod_ids = fields.One2many('mod', 'marque_id', string="Model", readonly=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tag already exists')
        
    ]