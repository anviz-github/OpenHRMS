# -*- coding: utf-8 -*-

import time
from datetime import datetime,date
from dateutil import relativedelta
from odoo import models, fields, api, _


class EmployeeInsurance(models.Model):
    _name = 'hr.insurance'
    _description = 'HR Insurance'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    policy_id = fields.Many2one('insurance.policy', string='Policy', required=True, help="Policy")
    amount = fields.Float(string='Premium', required=False, help="Policy amount")
    sum_insured = fields.Float(string="Sum Insured", required=False, help="Insured sum")
    policy_coverage = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                       required=True, default='monthly',
                                       string='Policy Coverage', help="During of the policy")
    company_amount = fields.Float(string='Company Amount', required=True, compute='_compute_amount', help="Company amount")
    personal_amount = fields.Float(string='Personal Amount', required=True, compute='_compute_amount', help="Personal amount")

    date_from = fields.Date(string='Date From',
                            default=time.strftime('%Y-%m-%d'), readonly=False, help="Start date")
    date_to = fields.Date(string='Date To',   readonly=False, help="End date",
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired'), ],
                             default='active', string="State", compute='get_status')
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)

    @api.onchange('policy_id')
    def _compute_amount(self):
        for record in self:
            for id in record.policy_id:
                if id.insure_type == "SIA":
                    record.company_amount = id.company_percentage/100 * record.employee_id.contract_id.sia
                    record.personal_amount = id.personal_percentage/100 * record.employee_id.contract_id.sia
                else:
                    record.company_amount = id.company_percentage/100 * record.employee_id.contract_id.hra
                    record.personal_amount = id.personal_percentage/100 * record.employee_id.contract_id.hra



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

    # @api.constrains('policy_coverage')
    # @api.onchange('policy_coverage')
    # def get_policy_period(self):
    #     for record in self:
    #         if self.policy_coverage == 'monthly':
    #             self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
    #         if self.policy_coverage == 'yearly':
    #             self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+12))[:10]


class HrInsurance(models.Model):
    _inherit = 'hr.employee'

    insurance_percentage = fields.Float(string="Company Percentage ", help="Company insurance percentage")
    deduced_amount_per_month = fields.Float(string="Salary deduced per month", compute="get_deduced_amount", help="Amount that is deduced from the salary per month")
    deduced_amount_per_year = fields.Float(string="Salary deduced per year", compute="get_deduced_amount", help="Amount that is deduced fronm the salary per year")
    insurance = fields.One2many('hr.insurance', 'employee_id', string="Insurance", help="Insurance",
                                domain=[('state', '=', 'active')])

    insurance_pesion_personal = fields.Float(string="pesion personal", compute="get_insure_subtotal")
    insurance_medical_personal = fields.Float(string="medical personal", compute="get_insure_subtotal")
    insurance_unemployment_personal = fields.Float(string="unemployment personal", compute="get_insure_subtotal")
    insurance_hf_personal = fields.Float(string="house fund personal", compute="get_insure_subtotal")
    insurance_fertility_personal = fields.Float(string="fertility personal", compute="get_insure_subtotal")
    insurance_injury_personal = fields.Float(string="injury personal", compute="get_insure_subtotal")
    insurance_pesion_company = fields.Float(string="pesion company", compute="get_insure_subtotal")
    insurance_medical_company = fields.Float(string="medical company", compute="get_insure_subtotal")
    insurance_unemployment_company = fields.Float(string="unemployment company", compute="get_insure_subtotal")
    insurance_hf_company = fields.Float(string="house fund company", compute="get_insure_subtotal")
    insurance_fertility_company = fields.Float(string="fertility company", compute="get_insure_subtotal")
    insurance_injury_company = fields.Float(string="injury company", compute="get_insure_subtotal")

    deduced_amount_company = fields.Float(string="Salary deduced company per month", compute="get_deduced_amount", help="Amount that is deduced from the salary company per month")
    deduced_amount_personal = fields.Float(string="Salary deduced personal per month", compute="get_deduced_amount",
                 help="Amount that is deduced from the salary personal per month")
    @api.onchange('insurance')
    def get_insure_subtotal(self):
        current_datetime = datetime.now()
        current_date = datetime.strftime(current_datetime, "%Y-%m-%d ")
        #lastMonth = (datetime.today().replace(day=1) - timedelta(days=1)).date()

        for emp in self:
            ins_amount_pesion_personal = 0
            ins_amount_pesion_company = 0
            ins_amount_medical_personal = 0
            ins_amount_medical_company = 0
            ins_amount_fertility_personal = 0
            ins_amount_fertility_company = 0
            ins_amount_hf_personal = 0
            ins_amount_hf_company = 0
            ins_amount_unemployment_personal = 0
            ins_amount_unemployment_company = 0
            ins_amount_injury_personal = 0
            ins_amount_injury_company = 0
            for ins in emp.insurance:
                x = str(ins.date_from)
                y = str(ins.date_to)
                if x < current_date:
                    if y >= current_date:
                        if ins.policy_id.name == "养老保险":
                            ins_amount_pesion_personal = ins_amount_pesion_personal + ins.personal_amount
                            ins_amount_pesion_company = ins_amount_pesion_company + ins.company_amount
                        elif ins.policy_id.name == "医疗保险":
                            ins_amount_medical_personal = ins_amount_medical_personal + ins.personal_amount
                            ins_amount_medical_company = ins_amount_medical_company + ins.company_amount
                        elif ins.policy_id.name == "失业保险":
                            ins_amount_unemployment_personal = ins_amount_unemployment_personal + ins.personal_amount
                            ins_amount_unemployment_company = ins_amount_unemployment_company + ins.company_amount
                        elif ins.policy_id.name == "生育保险":
                            ins_amount_fertility_personal = ins_amount_fertility_personal + ins.personal_amount
                            ins_amount_fertility_company = ins_amount_fertility_company + ins.company_amount
                        elif ins.policy_id.name == "工伤保险":
                            ins_amount_injury_personal = ins_amount_injury_personal + ins.personal_amount
                            ins_amount_injury_company = ins_amount_injury_company + ins.company_amount
                        elif ins.policy_id.name == "住房公积金":
                            ins_amount_hf_personal = ins_amount_hf_personal + ins.personal_amount
                            ins_amount_hf_company = ins_amount_hf_company + ins.company_amount

        emp.insurance_pesion_personal = ins_amount_pesion_personal
        emp.insurance_pesion_company = ins_amount_pesion_company
        emp.insurance_medical_personal = ins_amount_medical_personal
        emp.insurance_medical_company = ins_amount_medical_company
        emp.insurance_fertility_personal = ins_amount_fertility_personal
        emp.insurance_fertility_company = ins_amount_fertility_company
        emp.insurance_unemployment_personal = ins_amount_unemployment_personal
        emp.insurance_unemployment_company = ins_amount_unemployment_company
        emp.insurance_injury_personal = ins_amount_injury_personal
        emp.insurance_injury_company = ins_amount_injury_company
        emp.insurance_hf_personal = ins_amount_hf_personal
        emp.insurance_hf_company = ins_amount_hf_company
    def get_deduced_amount(self):
        self.deduced_amount_company = self.insurance_pesion_company + self.insurance_medical_company +\
                                      self.insurance_unemployment_company + self.insurance_hf_company +self.insurance_fertility_company + \
                                      self.insurance_injury_company
        self.deduced_amount_personal = self.insurance_pesion_personal + self.insurance_medical_personal + \
                                      self.insurance_unemployment_personal + self.insurance_hf_personal + self.insurance_fertility_personal + \
                                      self.insurance_injury_personal
        current_date = datetime.now()
        current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
        self.deduced_amount_per_month = self.deduced_amount_personal
            #self.deduced_amount_company + self.deduced_amount_personal
        self.deduced_amount_per_year = self.deduced_amount_per_month *12

        # for emp in self:
        #     ins_amount = 0
        #     for ins in emp.insurance:
        #         x = str(ins.date_from)
        #         y = str(ins.date_to)
        #         if x < current_datetime:
        #             if y > current_datetime:
        #                 if ins.policy_coverage == 'monthly':
        #                     ins_amount = ins_amount + (ins.deduced_amount_company+ins.deduced_amount_personal)*12
        #                 else:
        #                     ins_amount = ins_amount + ins.deduced_amount_company+ins.deduced_amount_personal
        #     emp.deduced_amount_per_year = ins_amount
        #                                   #-((ins_amount*emp.insurance_percentage)/100)
        #     emp.deduced_amount_per_month = emp.deduced_amount_per_year/12


class InsuranceRuleInput(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(InsuranceRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        for i in contract_ids:
            if contract_ids[0]:
                emp_id = contract_obj.browse(i[0].id).employee_id
                for result in res:
                    if emp_id.deduced_amount_per_month != 0:
                        if result.get('code') == 'INSUR':
                            result['amount'] = emp_id.deduced_amount_per_month

        return res
