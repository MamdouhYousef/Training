# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class new_module(models.Model):
    _name = 'new_module.new_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Html()
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
    file = fields.Binary('File')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    employee_ids = fields.One2many('hr.employee', 'new_module_id',)
    employee_m2m_ids = fields.Many2many('hr.employee', string='Employees M2M')
    activate = fields.Boolean('Active')
    total_other = fields.Float('Total')
    code = fields.Char('Code')
    leave_count = fields.Integer('Leave count', compute='get_leave_count')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name should be unique'),
    ]

    @api.one
    @api.depends('employee_id')
    def get_leave_count(self):
        leaves = self.env['hr.leave'].search([('employee_id','=', self.employee_id.id)])
        count = len(leaves)
        self.leave_count = count

    @api.multi
    def open_leave(self):
        return {
            'type': 'ir.actions.act_window',
            'name': "Leave",
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('employee_id','=', self.employee_id.id)],
        }


    @api.model
    def get_report_data(self):
        res = 9000
        return res

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

    @api.one
    def get_total(self):
        other_records = self.search([('value', '>=', 1000),])
        total = 0
        for rec in other_records:
            total = total + rec.value
        self.total_other = total

    def action_confirm(self):
        self.get_total()
        self.state = 'confirm'

    def action_refuse(self):
        self.state = 'refuse'

    def action_validate(self):
        female_employees = self.env['hr.employee'].search([('gender', '=', 'female')])
        total_childs = 0
        for emp in female_employees:
            total_childs += emp.children
        self.total_other = total_childs
        self.state = 'validate'

    def action_reset(self):
        self.state = 'draft'

    @api.model
    def create(self, vals_list):
        single_employees = self.env['hr.employee'].search([('marital','=','single')])
        total = 0
        for emp in single_employees:
            total += emp.children
            emp.children = False
        res = super(new_module, self).create(vals_list)
        res.total_other = total
        seq = self.env['ir.sequence'].next_by_code('new.module')
        res.code = seq
        return res

    @api.multi
    def write(self, vals):
        res = super(new_module, self).write(vals)
        return res


class Emlpoyee(models.Model):
    _inherit = "hr.employee"

    new_module_id = fields.Many2one('new_module.new_module', 'New Module')


