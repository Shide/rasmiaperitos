from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    first_visit_partner_latitude = fields.Float(
        string='First visit Contact Latitude',
        related='first_visit_partner_id.partner_latitude',
    )
    first_visit_partner_longitude = fields.Float(
        string='First visit Contact Longitude',
        related='first_visit_partner_id.partner_longitude',
    )
    first_visit_partner_is_geolocated = fields.Boolean(
        string='First Visit Geolocated',
        compute='_compute_first_visit_partner_is_geolocated',
        store=True,
    )

    @api.depends('first_visit_partner_latitude', 'first_visit_partner_longitude')
    def _compute_first_visit_partner_is_geolocated(self):
        for task in self:
            task.first_visit_partner_is_geolocated = task.first_visit_partner_latitude and \
                                                     task.first_visit_partner_longitude
