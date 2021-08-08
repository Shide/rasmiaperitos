import base64
import requests

from io import BytesIO
from zipfile import ZipFile
from odoo import _, api, exceptions, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def action_download_all_attachments(self):
        ptad_model = self.env['project.task.attachment.download']

        def create_zip_on_memory(content_l):
            in_memory = BytesIO()
            zf = ZipFile(in_memory, mode="w")
            for file_name, content in content_l:
                zf.writestr(file_name, content)
            zf.close()
            return in_memory.getvalue()

        content_list = []
        config_url = self.env["ir.config_parameter"].get_param(
            "web.base.url", default="https://rasmiaperitos.com"
        )
        base_url = config_url + '/web/binary/download_document'
        for task in self:
            response = requests.get(base_url + '?tab_id=%s&title=%s' % (task.attachment_ids.ids, task.display_name))
            if response.status_code == 200:
                content_list.append((task.display_name + '.zip', response.content))
                task.message_post(
                    body='%s Adjuntos descargados' % len(task.attachment_ids),
                    subject='Descarga de Adjuntos',
                    message_type='notification',
                )
        result = create_zip_on_memory(content_list)
        result_b64 = base64.b64encode(result)
        wizard = ptad_model.sudo().create({
            'name': fields.Date.to_string(fields.Date.today()) + '.zip',
            'content': result_b64,
        })
        action = self.env.ref('project_task_download_attachments.project_task_attachment_download_action').read()[0]
        action['res_id'] = wizard.id
        return action

    def action_view_all_attachments(self):
        attachments = self.mapped('attachment_ids')
        if not attachments:
            raise exceptions.UserError(_('No hay ningún adjunto que ver.'))

        action = self.env.ref('base.action_attachment').read()[0]
        action['domain'] = [('id', 'in', attachments.ids)]
        return action
