###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    deducibility_profile_id = fields.Many2one(
        comodel_name='account.deducibility.profile',
        string='Deduction Profile',
        ondelete='restrict',
    )
    l10n_es_autonomo_raw_vat = fields.Monetary(
        string='Original VAT',
        readonly=True,
        help='Total VAT amount before any deduction adjustment.',
    )
    l10n_es_autonomo_nd_vat = fields.Monetary(
        string='Non-deductible VAT',
        readonly=True,
        help='Portion of VAT reclassified as higher expense/asset value.',
    )

    @api.onchange('product_id', 'partner_id')
    def _onchange_l10n_es_autonomo_lookup(self):
        for line in self:
            if not line.move_id.is_purchase_document():
                continue
            profile = line.move_id.partner_id.l10n_es_autonomo_profile_id
            if not profile and line.product_id.l10n_es_autonomo_is_regulated:
                profile = line.product_id.l10n_es_autonomo_profile_id
            line.deducibility_profile_id = profile
