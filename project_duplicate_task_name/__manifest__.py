# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Task: Find duplicate names',
    'summary': 'Find duplicate names on tasks',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_task_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
