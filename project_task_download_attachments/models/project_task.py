from odoo import _, exceptions, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def action_download_all_attachments(self):
        self.ensure_one()
        if not self.attachment_ids:
            raise exceptions.UserError(_('No hay nada que descargar.'))

        self.message_post(
            body='%s Adjuntos descargados' % len(self.attachment_ids),
            subject='Descarga de Adjuntos',
            message_type='notification',
        )
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?tab_id=%s&title=%s' % (self.attachment_ids.ids, self.display_name),
            'target': 'new',
        }
