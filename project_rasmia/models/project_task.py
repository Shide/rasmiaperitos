from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Project
    color = fields.Integer(
        string='Color Index',
        related='project_id.color',
        store=True,
    )
    # Project Key
    key = fields.Char(
        string="Internal Ref.",
    )
    # Rasmia
    first_visit_date = fields.Datetime(
        string='First visit Date',
        help='Date to view the automobile for the first time'
    )
    first_visit_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='First visit Contact',
    )
    first_visit_partner_state_id = fields.Many2one(
        related='first_visit_partner_id.state_id',
        string='State of First visit',
        store=True,
    )
    first_visit_partner_city = fields.Char(
        related='first_visit_partner_id.city',
        string='City of First visit',
        store=True,
    )
    external_reference = fields.Char(
        string='External Ref.',
    )
    company_currency = fields.Many2one(
        comodel_name="res.currency",
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    bill_amount = fields.Monetary(
        string='Importe de la Minuta',
        currency_field='company_currency',
    )
