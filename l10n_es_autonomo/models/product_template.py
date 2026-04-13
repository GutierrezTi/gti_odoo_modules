###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_es_autonomo_is_regulated = fields.Boolean(
        string='Is Partially Deductible',
    )
    l10n_es_autonomo_profile_id = fields.Many2one(
        comodel_name='account.deducibility.profile',
        string='Product Deducibility Profile',
    )
