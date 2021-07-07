# Copyright 2021 Eduardo de Miguel (shide.shugo@gmail.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'DMS Directory: Download attachments',
    'summary': 'Download attachments from a dms directory',
    'version': '14.0.0',
    'category': 'Services/Project',
    'license': 'AGPL-3',
    'author': 'Eduardo de Miguel',
    'depends': [
        'dms',
        'download_multiple_attachments',
    ],
    'data': [
        'views/dms_directory_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
