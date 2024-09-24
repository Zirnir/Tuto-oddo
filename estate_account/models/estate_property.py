from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "test.model"

    def solding (self):
        super(EstateProperty, self).solding()

        sale_price = self.selling_price
        commission = sale_price * 0.06
        admin_fee = 100.00

        invoice_lines = [
            Command.create({
                'name': 'Commission (6%)',
                'quantity': 1,
                'price_unit': commission,
            }),
            Command.create({
                'name': 'Administrative Fee',
                'quantity': 1,
                'price_unit': admin_fee,
            }),
        ]

        move_values = {
            'partner_id': self.customer.id,
            'move_type': 'out_invoice',  
            'state': 'draft',
            'invoice_line_ids' : invoice_lines,
        }
        invoice = self.env['account.move'].create(move_values)
        return invoice