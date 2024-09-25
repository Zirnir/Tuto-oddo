from odoo import fields, models

class Mod(models.Model):
    _name = "mod"
    _description = "Models of Auto"

    name = fields.Char(required=True)

    auto_id = fields.One2many('auto', 'mod_id', string="Auto", readonly=True)
    marque_id = fields.Many2one("marque", string="Auto Type",required=True)

    option_ids = fields.Many2many("option", String="Options")
    

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tag already exists')
        
    ]