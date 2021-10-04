from odoo import _, api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    labor_price = fields.Monetary(
        string='Precio MO',
        currency_field='currency_id',
        help='Precio básico del coste de la mano de obra por hora.',
    )
    labor_pricelist = fields.Text(
        string='Tarifa MO',
        help='Tarifas de la mano de obra del taller.\n'
             'Se refiere al Precio MO en detalle si se requiere.',
    )
    opening_schedule = fields.Char(
        string='Horario de Apertura',
        help='Horario de apertura y atención al público.\n'
             'Ej.: L-V (08:00-14:00, 16:30-18:00), S (08:00-14:00)',
    )

    def _get_name(self):
        partner = self
        name = super()._get_name()

        if self._context.get('show_opening_schedule') and partner.opening_schedule:
            name += '\nHorario: %s' % partner.opening_schedule
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        return name
