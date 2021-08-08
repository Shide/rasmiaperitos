from odoo import fields, models


class ProjectTaskAttachmentDownload(models.TransientModel):
    _name = 'project.task.attachment.download'
    _description = 'Asistente de Descarga de Archivos adjuntos'

    name = fields.Char(
        string='Nombre del fichero',
    )
    content = fields.Binary(
        string="Content",
        attachment=True,
    )
