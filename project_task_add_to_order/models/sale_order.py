from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.task_id')
    def _compute_tasks_ids(self):
        for order in self:
            tasks = order.mapped('order_line.task_id')
            order.tasks_ids = tasks
            order.tasks_count = len(tasks)
