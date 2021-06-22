from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    duplicated_task_count = fields.Integer(
        string='Number of duplicated tasks',
        compute='_compute_duplicated_task_count',
        store=False,
    )

    def _compute_duplicated_task_count(self):
        pt_model = self.env['project.task'].sudo().with_context(active_test=False)
        for task in self:
            task.duplicated_task_count = pt_model.search_count([('name', 'ilike', task.name), ('id', '!=', task.id)])

    def action_open_duplicated_tasks(self):
        self.ensure_one()
        pt_model = self.env['project.task'].sudo().with_context(active_test=False)
        duplicated_tasks = pt_model.search([('name', 'ilike', self.name), ('id', '!=', self.id)])
        action = self.env.ref('project.action_view_all_task').read()[0]
        action['context'] = {}
        action['domain'] = [
            ('id', 'in', duplicated_tasks.ids),
            '|', ('active', '=', True), ('active', '=', False)
        ]
        return action
