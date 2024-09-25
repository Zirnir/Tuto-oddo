from odoo import fields, models

class Options(models.Model):
    _name = "option"
    _description = "Option"

    name = fields.Char(required=True)
    price = price = fields.Integer()

    mod_id = fields.Many2many("mod", String="Models")
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tag already exists')
        
    ]