# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# import json

# import requests
from re import match

from odoo import api, fields, models, exceptions


class ResUsers(models.Model):
    _inherit = 'res.users'

    president = fields.Boolean('Is President', default=False)
    secretary = fields.Boolean('Is Secretary', default=False)
    treasurer = fields.Boolean('Is Treasurer', default=False)
    manager = fields.Boolean('Is Manager', default=False)

    membership_ids = fields.One2many(
        comodel_name='membership',
        inverse_name='user_id',
        # domain=[('is_company', '=', False)],
        string='Memberships',
    )

    @api.onchange('secretary')
    def _on_change_secretary(self):
        if self.secretary:
            self.manager = True

    @api.onchange('treasurer')
    def _on_change_treasurer(self):
        if self.treasurer:
            self.manager = True

    @api.onchange('president')
    def _on_change_president(self):
        if self.president:
            self.manager = True

    @api.onchange('login')
    def validate_email(self):
        # import ipdb; ipdb.set_trace()
        if not self.login:
            return
        if not match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.login):
            raise exceptions.ValidationError('Invalid email address. Please enter a valid one.')
        if self.search_count([('login', '=', self.login), ]):
            raise exceptions.ValidationError('This email already exists. Please ')

    # @api.onchange('secretary')
    # def _onchange_status(self):
    #     self.groups_id = self.env['res.groups']
    #     #default_user or self.env['res.users']).sudo().groups_id
    #     # self.env['account.full.reconcile'].create({
    #     #     'partial_reconcile_ids': [(6, 0, partial_rec_ids)],
    #     #     'reconciled_line_ids': [(6, 0, self.ids)],
    #     #     'exchange_move_id': exchange_move.id if exchange_move else False,
    #     # })
