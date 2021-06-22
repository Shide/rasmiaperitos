from odoo import api, fields, models


class ProjectTaskWizardAddToOrder(models.TransientModel):
    _name = 'project.task.wizard.add.order'
    _description = 'Wizard to add tasks to orders'

    wizard_sale_line_ids = fields.One2many(
        comodel_name='project.task.wizard.add.order.line',
        inverse_name='wizard_id',
        string='Tasks to invoice',
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Selling Product for Order',
        domain=[('sale_ok', '=', True)],
        required=True,
    )

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if self.env.context.get('active_model') == 'project.task' and 'wizard_sale_line_ids' in fields:
            result['wizard_sale_line_ids'] = [(0, 0, {
                'task_id': task.id,
                'project_id': task.project_id.id,
                'stage_id': task.stage_id.id,
                'partner_id': task.partner_id.address_get(['invoice'])['invoice'],
                'sale_line_id': task.sale_line_id.id,
            }) for task in self.env['project.task'].browse(self.env.context.get('active_ids', []))]
        return result

    def confirm(self):
        orders = self.mapped('wizard_sale_line_ids.order_id')
        for wizard in self:
            partner_order = {}
            for line in wizard.wizard_sale_line_ids.filtered(lambda l: not l.task_id.sale_line_id):
                order = line.task_id.order_id or partner_order.get(line.task_id.partner_id)
                if not order:
                    order = line._create_related_order()
                    partner_order.setdefault(line.task_id.partner_id, order)
                    orders |= order
                line._create_related_order_line(order)
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['domain'] = [('id', 'in', orders.ids)]
        return action


class ProjectTaskWizardAddToOrderLine(models.TransientModel):
    _name = 'project.task.wizard.add.order.line'
    _description = 'Wizard lines to add tasks to orders'

    wizard_id = fields.Many2one(
        comodel_name='project.task.wizard.add.order',
        string='Wizard',
    )
    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        required=True,
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        readonly=True,
    )
    stage_id = fields.Many2one(
        comodel_name='project.task.type',
        string='Stage',
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        readonly=True,
    )
    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Sale Line',
        readonly=True,
    )
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order',
        domain=[('state', '=', 'draft')],
    )

    @api.onchange('sale_line_id')
    def onchange_sale_line_id(self):
        if self.sale_line_id:
            self.order_id = self.sale_line_id.order_id.id

    @api.onchange('task_id')
    def onchange_task_id(self):
        self.project_id = self.task_id.project_id.id
        self.partner_id = self.task_id.partner_id.id
        self.sale_line_id = self.task_id.sale_line_id.id
        self.stage_id = self.task_id.stage_id.id

    def _create_related_order(self):
        self.ensure_one()
        order = self.env['sale.order'].create({
            'partner_id': self.task_id.partner_id.id,
            'pricelist_id': self.task_id.partner_id.property_product_pricelist.id,
            'sale_order_template_id': self.task_id.partner_id.sale_order_template_invoiceable_task.id,
        })
        order.onchange_partner_id()
        order.onchange_sale_order_template_id()
        return order

    def _create_related_order_line(self, order):
        self.ensure_one()

        def _line_name_formatter(*args):
            return ' - '.join(list(filter(bool, args)))

        line_name = _line_name_formatter(
            self.task_id.external_reference,
            self.task_id.key,
            self.task_id.name,
        )

        order_line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.wizard_id.product_id.id,
            'name': line_name,
            'project_id': self.task_id.project_id.id,
            'task_id': self.task_id.id,
        })
        order_line.product_id_change()
        order_line.write({'name': line_name})
        self.task_id.write({
            'sale_order_id': order.id,
            'sale_line_id': order_line.id,
        })
        return order_line
