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
    # Insured
    insured_company_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('company_type', '=', 'company')],
        string='Compañía del Asegurado',
    )
    payment_commitment = fields.Boolean(
        string='Compromiso de pago',
    )
    franchise_amount = fields.Monetary(
        string='Importe de la Franquicia',
        currency_field='company_currency',
    )
    franchise_apply = fields.Boolean(
        string='Aplicar Franquicia',
    )
    policy_contract_date = fields.Date(
        string='Fecha de contratación de póliza',
    )
    policy_contract_effect = fields.Date(
        string='Fecha de efecto de póliza',
    )
    policy_mode = fields.Selection(
        string='Modalidad de póliza',
        selection=[
            ('terceros', 'Terceros'),
            ('terceros_ampliado', 'Terceros ampliado'),
            ('todo_riesgo', 'Todo riesgo'),
            ('todo_riesgo_franquicia', 'Todo riesgo con franquicia'),
            ('otro', 'Otro (Especificado en las notas)'),
        ],
    )
    insured_person_name = fields.Char(
        string='Nombre del asegurado',
    )
    insured_person_phone = fields.Char(
        string='Teléfono del asegurado',
    )
    tax_payable_by_insured = fields.Boolean(
        string='IVA a cargo del asegurado',
    )
    # Sinister
    sinister_date = fields.Date(
        string='Fecha del siniestro',
    )
    sinister_type = fields.Char(
        string='Tipo de siniestro'
    )
    sinister_damage_insured = fields.Text(
        string='Daños del vehículo asegurado',
    )
    sinister_version = fields.Text(
        string='Versión del siniestro',
    )
    opposing_vehicle = fields.Char(
        string='Vehículo contrario',
    )
    sinister_damage_opposing = fields.Text(
        string='Daños del vehículo contrario',
    )
