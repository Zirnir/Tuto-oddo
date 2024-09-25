from odoo import fields, models

class Type(models.Model):
    _name = "type"
    _description = "Types of Auto"

    name = fields.Char(required=True)

    auto_ids = fields.One2many('auto', 'type_id', string="Auto", readonly=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tag already exists')
        
    ]