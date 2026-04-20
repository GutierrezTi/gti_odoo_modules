###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import _, fields, http
from odoo.http import request


class IrpfAuditController(http.Controller):

    @http.route('/irpf/audit/response/<int:line_id>/<string:token>',
                auth='public', type='http', website=True)
    def irpf_audit_response(self, line_id, token, action=None, **post):
        line_sudo = request.env['account.irpf.audit.line'].sudo().search([
            ('id', '=', line_id),
            ('access_token', '=', token)
        ], limit=1)
        if not line_sudo:
            return request.render('website.404')
        if action == 'agree':
            line_sudo.write({
                'agreement_status': 'agreed',
                'response_date': fields.Datetime.now(),
                'state': 'matched' if line_sudo.period == 'annual' else line_sudo.state
            })
            header_msg = _(
                "Client %s has confirmed they AGREE with the IRPF audit."
            ) % line_sudo.partner_id.name
            line_sudo.audit_id.message_post(body=header_msg)
            line_sudo.message_post(body=_("Agreement received via portal."))
            return request.render(
                'l10n_es_irpf_reconciliation.response_thanks',
                {'status': 'agreed'})
        if action == 'disagree':
            if request.httprequest.method == 'POST' and post.get('reason'):
                line_sudo.write({
                    'agreement_status': 'disagreed',
                    'disagreement_reason': post.get('reason'),
                    'response_date': fields.Datetime.now(),
                    'state': 'discrepancy'
                })
                header_msg = _(
                    "ALERT: Client %s DISAGREES. Reason: %s"
                ) % (line_sudo.partner_id.name, post.get('reason'))
                line_sudo.audit_id.message_post(body=header_msg)
                line_sudo.message_post(body=_(
                    "Disagreement received. Reason: %s"
                ) % post.get('reason'))
                return request.render(
                    'l10n_es_irpf_reconciliation.response_thanks',
                    {'status': 'disagreed'})
            return request.render(
                'l10n_es_irpf_reconciliation.disagree_form',
                {'line': line_sudo}
            )
        return request.render('website.404')
