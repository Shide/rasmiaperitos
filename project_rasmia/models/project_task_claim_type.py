from odoo import models, fields, api, exceptions, _


class ProjectTaskClaimType(models.Model):
    _name = 'project.task.claim.type'

    name = fields.Char(
        string='Tipo de siniestro',
        required=True,
    )
    description = fields.Text(
        string='Descripción',
    )
