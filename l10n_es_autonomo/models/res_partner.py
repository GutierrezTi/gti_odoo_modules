###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_es_autonomo_profile_id = fields.Many2one(
        comodel_name='account.deducibility.profile',
        string='Default Deducibility Profile',
    )
