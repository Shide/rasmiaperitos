from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    track_kanban_state_time = fields.Boolean(
        string='Track Kanban State Time',
        default=False,
        help='This stage allows to record time spent on Task states.',
    )
