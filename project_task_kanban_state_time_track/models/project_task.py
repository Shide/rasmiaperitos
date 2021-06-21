from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checkpoint_kanban_state_normal = fields.Datetime(
        string='Checkpoint in progress',
        readonly=True,
    )
    checkpoint_kanban_state_done = fields.Datetime(
        string='Checkpoint ready',
        readonly=True,
    )
    checkpoint_kanban_state_blocked = fields.Datetime(
        string='Checkpoint blocked',
        readonly=True,
    )
    kanban_state_time_normal = fields.Float(
        string='Time spent in progress',
        readonly=True,
        help='Time spent on `normal` state.'
    )
    kanban_state_time_done = fields.Float(
        string='Time spent ready',
        readonly=True,
        help='Time spent on `done` state.'
    )
    kanban_state_time_blocked = fields.Float(
        string='Time spent blocked',
        readonly=True,
        help='Time spent on `blocked` state.'
    )

    def write(self, vals):
        if not ('kanban_state' in vals or 'stage_id' in vals):  #  or 'user_id' in vals
            return super().write(vals)

        ptt_model = self.env['project.task.type']

        def get_hours_until_now(dtt):
            return dtt and ((fields.Datetime.now() - dtt).total_seconds() / 3600.0) or 0.0

        res = []
        for task in self:
            task_vals = vals.copy()
            next_kanban_state = task_vals.get('kanban_state', task.kanban_state)
            next_stage = ptt_model.browse(task_vals.get('stage_id', task.stage_id.id))
            if next_stage != task.stage_id:  # Stage changes resets state
                next_kanban_state = 'normal'

            # TODO: Utilizar el horario de la persona asignada
            task_vals.update({
                'kanban_state_time_normal': task.kanban_state_time_normal + get_hours_until_now(
                    task.checkpoint_kanban_state_normal
                ),
                'kanban_state_time_done': task.kanban_state_time_done + get_hours_until_now(
                    task.checkpoint_kanban_state_done
                ),
                'kanban_state_time_blocked': task.kanban_state_time_blocked + get_hours_until_now(
                    task.checkpoint_kanban_state_blocked
                ),
            })
            next_checkpoint = next_stage.track_kanban_state_time and fields.Datetime.now()
            if next_kanban_state == 'normal':
                task_vals.update({
                    'checkpoint_kanban_state_normal': next_checkpoint,
                    'checkpoint_kanban_state_done': False,
                    'checkpoint_kanban_state_blocked': False,
                })
            elif next_kanban_state == 'done':
                task_vals.update({
                    'checkpoint_kanban_state_normal': False,
                    'checkpoint_kanban_state_done': next_checkpoint,
                    'checkpoint_kanban_state_blocked': False,
                })
            elif next_kanban_state == 'blocked':
                task_vals.update({
                    'checkpoint_kanban_state_normal': False,
                    'checkpoint_kanban_state_done': False,
                    'checkpoint_kanban_state_blocked': next_checkpoint,
                })
            res.append(super(ProjectTask, task).write(task_vals))
        return all(res)
