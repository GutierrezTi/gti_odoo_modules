###############################################################################
#    GutierrezTI Team
#    Copyright (C) 2026-Today GutierrezTI Team <www.gutierrezti.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
{
    'name': 'Spain - IRPF Reconciliation & Audit',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Audit and reconcile IRPF retentions against AEAT fiscal data',
    'description': """
        IRPF retention discrepancies between Odoo accounting and AEAT data.
        Features:
        - Manual/Bulk registration of AEAT data.
        - Automatic calculation of Odoo retentions via account.move.line.
        - Bulk notification system for discrepancies (OCA 347 style).
    """,
    'author': 'GutierrezTi Team',
    'website': 'https://gutierrezti.es',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'mail',
        'l10n_es'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_irpf_import_wizard_views.xml',
        'views/account_irpf_audit_line_views.xml',
        'views/account_irpf_audit_views.xml',
        'views/portal_templates.xml',
        'report/irpf_audit_reports.xml',
        'report/irpf_audit_report_templates.xml',
        'data/mail_template_data.xml',
    ],
}
