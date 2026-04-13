###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import fields, models


class AccountDeducibilityProfile(models.Model):
    _name = 'account.deducibility.profile'
    _description = 'Spanish Autónomo Deducibility Profile'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    vat_ratio = fields.Float(
        string='VAT Deductible %',
        default=100.0,
        help='Percentage of VAT that is legally deductible.',
    )
    expense_ratio = fields.Float(
        string='Expense Deductible %',
        default=100.0,
        help='Percentage of the expense that is deductible for IRPF.',
    )
    reclassification_strategy = fields.Selection(
        selection=[
            ('base_line', 'Add to Base Line (Higher Expense/Asset)'),
            ('specific_account', 'Move to Specific Account'),
        ],
        string='VAT Reclassification Strategy',
        default='base_line',
        required=True,
    )
    specific_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Specific Account',
        company_dependent=True,
    )
    active = fields.Boolean(
        default=True,
    )
