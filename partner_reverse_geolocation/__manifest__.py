# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Reverse Geolocalize',
    'summary': 'Partner Reverse Geolocalize',
    'version': '14.0.0',
    'category': 'Hidden/Tools',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'base',
        'base_geolocalize',
    ],
    'external_dependencies': {
        'python': ['googlemaps>=4.4.5'],
    },
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
