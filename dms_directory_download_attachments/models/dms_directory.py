from odoo import _, exceptions, models


class DmsDirectory(models.Model):
    _inherit = "dms.directory"

    def action_download_all_attachments(self):
        attachments = self.mapped('file_ids.attachment_id')
        if not attachments:
            raise exceptions.UserError(_('No hay nada que descargar.'))
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?tab_id=%s' % attachments.ids,
            'target': 'new',
        }
