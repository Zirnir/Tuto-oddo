from odoo import fields, models

class Tag(models.Model):
    _name = "tag"
    _description = "Tag of property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index", default=0)
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tag already exists')
        
    ]