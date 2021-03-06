from datetime import timedelta

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
    first_visit_partner_labor_price = fields.Monetary(
        related='first_visit_partner_id.labor_price',
        currency_field='company_currency',
        readonly=True,
    )
    first_visit_partner_labor_pricelist = fields.Text(
        related='first_visit_partner_id.labor_pricelist',
        readonly=True,
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
    forfait_km_amount = fields.Monetary(
        string='Importe Forfait KM',
        currency_field='company_currency',
        help="Importe del Forfait que abona la compañía para compensar el kilometraje al ser fuera de la capital",
    )
    # Insured
    insured_company_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('company_type', '=', 'company')],
        string='Compañía del Asegurado',
    )
    insured_company_image_1920 = fields.Binary(
        string="Imagen compañía aseguradora",
        compute='_compute_image',
        compute_sudo=True,
        store=True
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
    claim_type_id = fields.Many2one(
        comodel_name='project.task.claim.type',
        string='Tipo de siniestro',
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

    @api.depends('insured_company_id.image_1920')
    def _compute_image(self):
        for task in self:
            # We have to be in sudo to have access to the images
            partner = self.sudo().env['res.partner'].browse(task.insured_company_id.id)
            task.insured_company_image_1920 = partner and partner.image_1920 or None

    def set_next_date_deadline(self):
        for task in self:
            task.date_deadline = fields.Date.today() + timedelta(days=7)

    def update_date_end(self, stage_id):
        res = super().update_date_end(stage_id)
        project_task_type = self.env['project.task.type'].browse(stage_id)
        if project_task_type.is_closed:
            res.update({'date_deadline': False})
        return res
