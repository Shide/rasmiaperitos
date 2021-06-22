# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Add Tasks to Sale Orders',
    'summary': 'Add Tasks to Sale Orders from the Task views',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'base',
        'project',
        'sale_project',
        'project_key',
        'project_rasmia',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'wizard/project_task_wizard_add_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
