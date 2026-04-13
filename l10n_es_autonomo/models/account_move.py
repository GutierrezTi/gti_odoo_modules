###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import Command, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_es_autonomo_vat_deductible = fields.Monetary(
        string='Deductible VAT',
        compute='_compute_l10n_es_autonomo_totals',
        currency_field='currency_id',
    )
    l10n_es_autonomo_expense_total = fields.Monetary(
        string='Total Fiscal Expense',
        compute='_compute_l10n_es_autonomo_totals',
        currency_field='currency_id',
    )

    @api.depends(
        'invoice_line_ids.deducibility_profile_id',
        'invoice_line_ids.tax_ids',
        'invoice_line_ids.price_subtotal',
    )
    def _compute_l10n_es_autonomo_totals(self):
        for move in self:
            vat_deductible = 0.0
            expense_total = 0.0
            if move.move_type in ('in_invoice', 'in_refund'):
                for line in move.invoice_line_ids:
                    line_taxes = line.tax_ids.compute_all(
                        price_unit=line.price_subtotal,
                        currency=move.currency_id,
                        quantity=1.0,
                        product=line.product_id,
                        partner=move.partner_id,
                        is_refund=(move.move_type == 'in_refund')
                    )
                    total_vat_line = sum(
                        t['amount'] for t in line_taxes['taxes'] if
                        t['amount'] > 0)
                    profile = line.deducibility_profile_id
                    if profile:
                        vat_ratio = profile.vat_ratio if (
                            profile.vat_ratio <= 1.0) else (
                            profile.vat_ratio / 100.0)
                        exp_ratio = profile.expense_ratio if (
                            profile.expense_ratio <= 1.0) else (
                            profile.expense_ratio / 100.0)
                        ded_vat = total_vat_line * vat_ratio
                        non_ded_vat = total_vat_line - ded_vat
                        vat_deductible += ded_vat
                        expense_total += (line.price_subtotal + non_ded_vat
                                          ) * exp_ratio
                    else:
                        vat_deductible += total_vat_line
                        expense_total += line.price_subtotal
            move.l10n_es_autonomo_vat_deductible = vat_deductible
            move.l10n_es_autonomo_expense_total = expense_total

    def _post(self, soft=True):
        for move in self.filtered(
                lambda m: m.is_purchase_document() and m.state == 'draft'):
            move._l10n_es_autonomo_apply_reclassification()
        return super()._post(soft=soft)

    def _l10n_es_autonomo_apply_reclassification(self):
        self.ensure_one()
        commands = []
        for line in self.invoice_line_ids.filtered('deducibility_profile_id'):
            profile = line.deducibility_profile_id
            vat_ratio = profile.vat_ratio if (
                profile.vat_ratio <= 1.0) else profile.vat_ratio / 100.0
            if vat_ratio >= 1.0:
                continue
            tax_lines = self.line_ids.filtered(
                lambda ln: ln.tax_line_id in line.tax_ids and abs(
                    ln.tax_base_amount - line.price_subtotal) < 0.01)
            total_raw_vat = sum(abs(ln.balance) for ln in tax_lines)
            total_nd_vat = 0.0
            for t_line in tax_lines:
                nd_vat = t_line.balance * (1 - vat_ratio)
                if nd_vat:
                    total_nd_vat += nd_vat
                    commands.append(Command.update(t_line.id, {
                        'debit': t_line.debit - nd_vat if
                        t_line.debit > 0 else 0.0,
                        'credit': t_line.credit + nd_vat if
                        t_line.credit < 0 else 0.0,
                    }))
            if total_nd_vat:
                line_update_vals = {
                    'l10n_es_autonomo_raw_vat': total_raw_vat,
                    'l10n_es_autonomo_nd_vat': abs(total_nd_vat),
                }
                if profile.reclassification_strategy == 'base_line':
                    line_update_vals.update({
                        'debit': line.debit + total_nd_vat if
                        line.debit > 0 else 0.0,
                        'credit': line.credit - total_nd_vat if
                        line.credit < 0 else 0.0,
                    })
                commands.append(Command.update(line.id, line_update_vals))
                if profile.reclassification_strategy == 'specific_account':
                    commands.append(Command.create({
                        'name': self.env._(
                            'Non-deductible VAT: %s' % line.name),
                        'account_id': profile.specific_account_id.id,
                        'debit': total_nd_vat if line.debit > 0 else 0.0,
                        'credit': abs(
                            total_nd_vat) if line.credit > 0 else 0.0,
                        'partner_id': self.partner_id.id,
                    }))
        if commands:
            self.write({'line_ids': commands})
