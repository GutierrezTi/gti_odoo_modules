###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import api, fields, models


class AccountIrpfAudit(models.Model):
    _name = 'account.irpf.audit'
    _description = 'IRPF Annual & Quarterly Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fiscal_year desc, period'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        related='company_id.currency_id',
    )
    fiscal_year = fields.Char(
        string='Fiscal Year',
        required=True,
        tracking=True,
        default=lambda self: str(fields.Date.context_today(self).year),
    )
    period = fields.Selection(
        selection=[
            ('1Q', '1Q (Jan - Mar)'),
            ('2Q', '2Q (Apr - Jun)'),
            ('3Q', '3Q (Jul - Sep)'),
            ('4Q', '4Q (Oct - Dec)'),
            ('annual', 'Annual (Model 190)'),
        ],
        string='Period',
        required=True,
        default='annual',
        tracking=True,
    )
    line_ids = fields.One2many(
        comodel_name='account.irpf.audit.line',
        inverse_name='audit_id',
        string='Audit Lines',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('calculated', 'Calculated'),
            ('done', 'Closed'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    @api.depends('fiscal_year', 'period')
    def _compute_name(self):
        for rec in self:
            period_label = dict(self._fields['period'].selection).get(
                rec.period, '')
            rec.name = f"IRPF {period_label} - {rec.fiscal_year}" if (
                rec.fiscal_year) else 'New Audit'

    def _get_date_range(self):
        self.ensure_one()
        year = int(self.fiscal_year)
        if self.period == '1Q':
            return f'{year}-01-01', f'{year}-03-31'
        if self.period == '2Q':
            return f'{year}-04-01', f'{year}-06-30'
        if self.period == '3Q':
            return f'{year}-07-01', f'{year}-09-30'
        if self.period == '4Q':
            return f'{year}-10-01', f'{year}-12-31'
        return f'{year}-01-01', f'{year}-12-31'

    def action_calculate(self):
        self.ensure_one()
        self.line_ids.unlink()
        start_date, end_date = self._get_date_range()
        domain = [
            ('company_id', '=', self.company_id.id),
            ('move_id.state', '=', 'posted'),
            ('account_id.code', '=like', '473%'),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ]
        groups = self.env['account.move.line']._read_group(
            domain, ['partner_id'], ['balance:sum'])
        lines_to_create = [{
            'audit_id': self.id,
            'partner_id': partner.id,
            'amount_odoo': balance_sum,
        } for partner, balance_sum in groups if partner]
        if lines_to_create:
            self.env['account.irpf.audit.line'].create(lines_to_create)
        self.state = 'calculated'

    def action_open_import_wizard(self):
        self.ensure_one()
        return {
            'name': self.env._('Import AEAT Data'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.irpf.import.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_audit_id': self.id},
        }

    def action_send_notifications(self):
        self.ensure_one()
        template_info = self.env.ref(
            'l10n_es_irpf_reconciliation.email_template_irpf_quarterly_info',
            raise_if_not_found=False)
        template_disc = self.env.ref(
            'l10n_es_irpf_reconciliation.email_template_irpf_annual_discrepancy',
            raise_if_not_found=False)
        if not template_info or not template_disc:
            return
        sent_count = 0
        for line in self.line_ids:
            if not line.partner_id.email:
                continue
            if line.period != 'annual' and line.state == 'info':
                template_info.send_mail(line.id, force_send=False)
                line.state = 'notified'
                sent_count += 1
            elif line.period == 'annual' and line.state == 'discrepancy':
                template_disc.send_mail(line.id, force_send=False)
                line.state = 'notified'
                sent_count += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': self.env._('Notifications Queued'),
                'message': self.env._(
                    '%s emails have been added to the queue. They will be '
                    'sent automatically.') % sent_count,
                'type': 'success',
                'sticky': False,
            }
        }

    def action_close_audit(self):
        self.ensure_one()
        self.state = 'done'

    def action_draft(self):
        self.ensure_one()
        self.line_ids.unlink()
        self.state = 'draft'
