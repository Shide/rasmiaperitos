from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_template_invoiceable_task = fields.Many2one(
        comodel_name='sale.order.template',
        string='Order Template for Task invoicing',
        help='Project template that will be loaded by default when creating sales orders from tasks',
    )
