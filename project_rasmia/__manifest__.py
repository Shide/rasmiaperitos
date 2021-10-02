# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project: Rasmia Peritos',
    'summary': 'Project customization for Rasmia Peritos',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'base',
        'project',
        'project_key',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/project_task_view.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
