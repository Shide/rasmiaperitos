from odoo import _, api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    labor_price = fields.Monetary(
        string='Precio Mano de obra',
        currency_field='currency_id',
        help='Precio del coste de la mano de obra por hora.',
    )
    opening_schedule = fields.Char(
        string='Horario de Apertura',
        help='Horario de apertura y atención al público.\n'
             'Ej.: L-V (08:00-14:00, 16:30-18:00), S (08:00-14:00)',
    )

    def _get_name(self):
        partner = self
        name = super()._get_name()

        if self._context.get('show_labor_price') and partner.labor_price:
            name += '\nPrecio MO: %s%s' % (partner.currency_id.round(partner.labor_price), partner.currency_id.symbol)
        if self._context.get('show_opening_schedule') and partner.opening_schedule:
            name += '\nHorario: %s' % partner.opening_schedule
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        return name
