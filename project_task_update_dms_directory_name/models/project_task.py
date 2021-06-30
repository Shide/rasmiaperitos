from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def write(self, vals):
        res = super().write(vals)
        if vals.get("project_id", False) or vals.get("name", False):
            dd_model = self.env['dms.directory']
            for task in self:
                dd_model.search([
                    ('res_model', '=', 'project.task'),
                    ('res_id', '=', task.id),
                ]).write({'name': task.display_name})
        return res
