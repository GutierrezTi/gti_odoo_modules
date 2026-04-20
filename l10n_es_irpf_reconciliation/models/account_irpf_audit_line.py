###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
import uuid

from odoo import api, fields, models


class AccountIrpfAuditLine(models.Model):
    _name = 'account.irpf.audit.line'
    _description = 'IRPF Audit Line'
    _order = 'difference desc, partner_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )

    audit_id = fields.Many2one(
        comodel_name='account.irpf.audit',
        string='Audit',
        ondelete='cascade',
    )
    period = fields.Selection(
        related='audit_id.period',
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
    )
    currency_id = fields.Many2one(
        related='audit_id.currency_id',
    )
    amount_odoo = fields.Monetary(
        string='Odoo',
        currency_field='currency_id',
    )
    amount_aeat = fields.Monetary(
        string='AEAT',
        currency_field='currency_id',
        tracking=True,
    )
    difference = fields.Monetary(
        string='Diff',
        compute='_compute_difference',
        store=True,
        currency_field='currency_id',
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('info', 'Informative'),
            ('pending', 'Pending AEAT'),
            ('matched', 'Matched'),
            ('discrepancy', 'Discrepancy'),
            ('notified', 'Notified'),
        ],
        string='Status',
        compute='_compute_state',
        store=True,
        tracking=True,
    )
    access_token = fields.Char(
        string='Access Token',
        default=lambda self: str(uuid.uuid4()),
        copy=False,
    )
    agreement_status = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('agreed', 'Agreed'),
            ('disagreed', 'Disagreed')
        ],
        string='Client Response',
        default='pending',
        tracking=True,
    )
    disagreement_reason = fields.Text(
        string='Discrepancy Reason',
        tracking=True,
    )
    response_date = fields.Datetime(
        string='Response Date',
    )

    @api.depends('partner_id', 'audit_id.fiscal_year', 'audit_id.period')
    def _compute_name(self):
        for rec in self:
            if rec.partner_id and rec.audit_id:
                period_str = f" ({rec.period})" if rec.period != 'annual' else ""
                rec.name = (f"{rec.partner_id.name} - "
                            f"{rec.audit_id.fiscal_year}{period_str}")
            else:
                rec.name = "New Audit Line"

    def _get_share_url(self, action):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        return (f"{base_url}/irpf/audit/response/{self.id}/"
                f"{self.access_token}?action={action}")

    @api.depends('amount_odoo', 'amount_aeat')
    def _compute_difference(self):
        for rec in self:
            rec.difference = rec.amount_odoo - rec.amount_aeat

    @api.depends('difference', 'amount_aeat', 'period')
    def _compute_state(self):
        for rec in self:
            if rec.period != 'annual':
                rec.state = 'info'
            elif rec.amount_aeat == 0.0:
                rec.state = 'pending'
            elif abs(rec.difference) <= 0.05:
                rec.state = 'matched'
            else:
                rec.state = 'discrepancy'

    def _get_invoice_details(self):
        self.ensure_one()
        start_date, end_date = self.audit_id._get_date_range()
        return self.env['account.move.line'].search([
            ('partner_id', '=', self.partner_id.id),
            ('company_id', '=', self.audit_id.company_id.id),
            ('move_id.state', '=', 'posted'),
            ('account_id.code', '=like', '473%'),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ], order='date asc')

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref(
            'l10n_es_irpf_reconciliation.action_report_irpf_details').with_context(
            lang=self.partner_id.lang).report_action(self)

    def action_send_manual_email(self):
        self.ensure_one()
        if self.period != 'annual':
            template = self.env.ref(
                'l10n_es_irpf_reconciliation.email_template_irpf_quarterly_info',
                raise_if_not_found=False)
        else:
            template = self.env.ref(
                'l10n_es_irpf_reconciliation.email_template_irpf_annual_discrepancy',
                raise_if_not_found=False)
        if not template:
            return
        ctx = {
            'default_model': 'account.irpf.audit.line',
            'default_res_ids': self.ids,
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'force_email': True,
            'lang': self.partner_id.lang,
        }
        return {
            'name': self.env._('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_open_line(self):
        self.ensure_one()
        return {
            'name': self.env._('Client Audit Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.irpf.audit.line',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def action_view_invoices(self):
        self.ensure_one()
        start_date, end_date = self.audit_id._get_date_range()
        return {
            'name': self.env._('Related Invoices: %s') % self.partner_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line',
            'view_mode': 'list,form',
            'domain': [
                ('partner_id', '=', self.partner_id.id),
                ('company_id', '=', self.audit_id.company_id.id),
                ('move_id.state', '=', 'posted'),
                ('account_id.code', '=like', '473%'),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
            ],
            'context': {'create': False},
        }
