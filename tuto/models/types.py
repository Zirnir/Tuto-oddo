from odoo import fields, models

class Types(models.Model):
    _name = "types"
    _description = "Types of Property"
    _order = "name"

    name = fields.Char(required=True)

    property_id = fields.One2many('test.model', 'types', string="Property", readonly=True)
    offer_ids = fields.One2many('offer', 'types', readonly=True)

    offer_count = fields.Integer(compute='_compute_offer_count')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'This tupe already exists')
        
    ]

    # def stat(self):
    #     for record in self:
            