# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project: Rasmia Task First Visit Geolocation',
    'summary': 'Project Task First Visit Geolocation',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'project',
        'web_google_maps',
        'project_rasmia',
    ],
    'data': [
        'views/project_task_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
