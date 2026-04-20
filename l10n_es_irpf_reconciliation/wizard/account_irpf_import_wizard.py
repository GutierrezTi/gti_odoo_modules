###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
import base64
import csv
import io

from odoo import fields, models
from odoo.exceptions import UserError


class AccountIrpfImportWizard(models.TransientModel):
    _name = 'account.irpf.import.wizard'
    _description = 'Import AEAT Data Wizard'

    audit_id = fields.Many2one(
        comodel_name='account.irpf.audit',
        string='Audit Reference',
        required=True,
    )
    data_file = fields.Binary(
        string='CSV File',
        required=True,
        help="Upload the AEAT CSV file. Columns must be: VAT, Amount",
    )
    filename = fields.Char(
        string='Filename',
    )

    def action_import(self):
        self.ensure_one()
        if not self.data_file:
            raise UserError(self.env._("Please upload a CSV file."))

        try:
            csv_data = base64.b64decode(self.data_file).decode('utf-8-sig')
            reader = csv.reader(io.StringIO(csv_data), delimiter=';')
        except Exception as e:
            raise UserError(self.env._(
                "Invalid file format. Please ensure it is a valid CSV file "
                "saved with UTF-8 encoding. Error: %s") % e)
        lines_by_vat = {
            (line.partner_id.vat or '').replace('ES', '').strip().upper(): line
            for line in self.audit_id.line_ids
        }
        updated_count = 0
        for row in reader:
            if not row or len(row) < 2:
                continue
            vat = row[0].strip().upper().replace('ES', '')
            amount_str = row[1].strip()
            if not vat or vat not in lines_by_vat:
                continue
            try:
                amount_clean = amount_str.replace('.', '').replace(',', '.')
                amount = float(amount_clean)
            except ValueError:
                continue
            lines_by_vat[vat].amount_aeat = amount
            updated_count += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': self.env._('Import Successful'),
                'message': self.env._(
                    '%s records updated from the AEAT file.') % updated_count,
                'type': 'success',
                'sticky': False,
            }
        }
