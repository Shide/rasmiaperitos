# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Task: Report',
    'summary': 'Report for Rasmia Project Tasks',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'project',
        'project_rasmia',
    ],
    'data': [
        'views/project_task_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
