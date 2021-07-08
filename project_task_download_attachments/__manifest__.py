# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Task: Download attachments',
    'summary': 'Download attachments from a project task',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'project',
        'download_multiple_attachments',
    ],
    'data': [
        'views/project_task_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
