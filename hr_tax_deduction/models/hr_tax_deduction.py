# -*- coding: utf-8 -*-
import  time
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
#from odoo import tools, _


class TaxDeduction(models.Model):
    _name = 'hr.tax.deduction'
    _description = 'Tax Deduction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    #name = fields.Char(string="Tax Deduction Name", required=True)
    name = fields.Selection(
        [('子女教育支出', "Children's Education Expenditure"), ('住房租金支出',"Housing Rent Expenditure"), ('房屋贷款利息支出',"Housing Loan Interest Expenses"), ('赡养老人支出', "Retire Support Expenses"), ('继续教育支出', "Continuing Education Expenditure")],
        required=True, default='子女教育支出',
        string='专项扣除', help="扣除种类")
    deduction_amount = fields.Float(string='Deduction Amount', required=True, help="扣除金额")
    date_from = fields.Date(string='Date From',
                            default=time.strftime('%Y-%m-%d'), readonly=False, help="Start date")
    date_to = fields.Date(string='Date To', readonly=False, help="End date",
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired'), ],
                             default='active', string="State", compute='get_status')
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.company.id)
    def get_status(self):
        current_datetime = datetime.now()
        current_date = datetime.strftime(current_datetime, "%Y-%m-%d ")


        for i in self:
            x = str(i.date_from)
            y = str(i.date_to)
            if x <= current_date:
                if y >= current_date:
                    i.state = 'active'
                else:
                    i.state = 'expired'
class HrInsurance(models.Model):
    _inherit = 'hr.employee'
    deduction_total = fields.Float(string="Tax Deduction", default=0, compute="get_tax_deduction_total")
    deduction = fields.One2many('hr.tax.deduction', 'employee_id', string="Tax_Deduction", help="Tax Deduction",)
                                #domain=[('state', '=', 'active')])


    @api.onchange('deduction')
    def get_tax_deduction_total(self):
        # current_date = datetime.now()
        # current_date = datetime.strftime(current_date, "%Y-%m-%d ")


        lastMonth = (datetime.today().replace(day=1) - timedelta(days=1)).date()
        #current_date = datetime.strftime(lastMonth, "%Y-%m-%d ")

        for emp in self:
            ins_amount = 0
            for ins in emp.deduction:
                x = ins.date_from
                y = ins.date_to
                if x < lastMonth:
                    if y >= lastMonth:
                        ins_amount = ins_amount + ins.deduction_amount
        emp.deduction_total = ins_amount