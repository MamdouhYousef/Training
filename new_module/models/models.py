# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class new_module(models.Model):
    _name = 'new_module.new_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    type = fields.Selection([
        ('type1', 'Type1'),
        ('type2', 'Type2'),
        ('type3', 'Type3'),
    ], string="Type")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('validate', 'Validate'),
        ('refuse', 'Refuse'),
    ], string="Status", default='draft')
    date = fields.Date()
    date_time = fields.Datetime()

    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'type2':
            self.value = 100
        else:
            self.value = False

    @api.constrains('type', 'value')
    def check_value(self):
        if self.type == 'type1' and self.value < 50:
            raise ValidationError('When Type 1 value must be greater than 50 !')

    @api.one
    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

    def action_confirm(self):
        self.state = 'confirm'

    def action_refuse(self):
        self.state = 'refuse'

    def action_validate(self):
        self.state = 'validate'

    def action_reset(self):
        self.state = 'draft'
        
    def create(self, vals_list):
        #do somthing
        res = super(new_module, self).create(vals_list)
        return res
