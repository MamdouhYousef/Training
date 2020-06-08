# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"

    id_expiry_date = fields.Date('Id expiry date')
    id_issue_date = fields.Date('ID Issue date')
    passport_expiry_date = fields.Date('passport expiry date')
    passport_issue_date = fields.Date('passport Issue date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], string="Status", default='draft')

    @api.one
    def action_confirm(self):
        self.state = 'confirm'