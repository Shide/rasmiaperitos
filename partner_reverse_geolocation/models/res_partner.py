import googlemaps

from odoo import _, api, exceptions, fields, models

RTYPES = ['car_repair', 'establishment', 'street_address']  # Sorted by priority
ADD_TYPE_FIELD_MAP = {
    'street_number': 'number',
    'route': 'route',
    'postal_code': 'postal_code',
    'locality': 'city',
    'administrative_area_level_2': 'state',
}


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _reverse_geo_localize(self, gmaps_client, latitude, longitude, result_types=None):
        rcz_model = self.env['res.city.zip']
        rcs_model = self.env['res.country.state']

        country_id = self.env.user.company_id.country_id.id
        result_types = result_types or RTYPES
        for address_data in sorted(gmaps_client.reverse_geocode((longitude, latitude), result_type=result_types),
                                   key=lambda g: result_types[-1] in g['types'],
                                   reverse=True):
            address_dict = dict.fromkeys(ADD_TYPE_FIELD_MAP.values(), '')
            address_dict['country_id'] = country_id
            for address_component in address_data['address_components']:
                for address_type in address_component['types']:
                    address_field = ADD_TYPE_FIELD_MAP.get(address_type)
                    if address_field:
                        address_dict[address_field] = address_component['long_name']

            if address_dict['route'] and (address_dict['postal_code'] or (address_dict['city'], address_dict['state'])):
                address_dict['street'] = ', '.join(list(filter(bool, [address_dict.pop('route'), address_dict.pop('number')])))
                address_dict['zip_id'] = rcz_model.search([('name', '=', address_dict.pop('postal_code'))], limit=1).id
                address_dict['state_id'] = rcs_model.search([('name', 'ilike', address_dict.pop('state'))], limit=1).id
                return address_dict

    def reverse_geo_localize(self):
        gmaps_apikey = self.env['ir.config_parameter'].sudo().get_param('base_geolocalize.google_map_api_key',)
        if not gmaps_apikey:
            raise exceptions.UserError(_('You should provide Google Maps API key'))
        gmaps_client = googlemaps.Client(key=gmaps_apikey)
        for partner in self:
            if partner.partner_latitude and partner.partner_longitude:
                result = partner._reverse_geo_localize(gmaps_client, partner.partner_longitude, partner.partner_latitude)
                if result:
                    partner.write(result)
        return True
