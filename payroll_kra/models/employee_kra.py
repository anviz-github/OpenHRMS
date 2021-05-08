#-*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class payroll_kra(models.Model):
    _inherit = 'hr.employee'

    kra_final_score_this_month = fields.Float(compute='_kra_final_score_compute', string='This Month Final Score' \
                                              , default=100, readonly='1')
    #    , store=True)

    kra_final_score_last_month = fields.Float(compute='_kra_final_score_compute', string='Last Month Final Score' \
                                              , default=100, readonly='1')
    #    , store=True)

    kras = fields.One2many('employee.kra', 'employee_id', string="KRAS", help="KRAS", compute='_get_kras')
                          #domain=[('state', '=', 'done')])

    def _get_kras(self):
        months = []
        this_month = datetime.now().month
        year = datetime.now().year
        months.append(this_month)
        if this_month == 1:
            last_month = 12
            year = year - 1
        else:
            last_month = this_month - 1
        months.append(last_month)

        for rec in self:

            kra = self.env['employee.kra'].search([('employee_id', '=', rec.id), ('state', '=', 'done'), ('year', '=', str(year)), ('name', 'in', months)])
            rec.kras = kra



    def _kra_final_score_compute(self):
        this_month = datetime.now().month
        year = datetime.now().year
        if this_month == 1:
            last_month = 12
            year = year - 1
        else:
            last_month = this_month - 1

        for emp in self:
            final_score_this = 0
            final_score_last = 0

            this_records = 0
            last_records = 0
            for kra_id in emp.kras:



                if kra_id.name == str(this_month) and kra_id.year.name == str(year):
                    this_records += 1
                elif kra_id.name == str(last_month) and kra_id.year.name == str(year):
                    last_records += 1

                questions = self.env['employee.kra.question'].search([('employee_kra_id', '=', kra_id.id)])

                for question in questions:
                    if kra_id.name == str(this_month):
                        final_score_this = final_score_this + question.final_score
                    else:
                        final_score_last = final_score_last + question.final_score

           
            if last_records == 0:
                last_records = 1
            if this_records == 0:
                this_records = 1

            emp.kra_final_score_last_month = final_score_last / last_records
            emp.kra_final_score_this_month = final_score_this / this_records


