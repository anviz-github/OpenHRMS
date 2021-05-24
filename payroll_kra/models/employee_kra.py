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
    kra_final_score_this_quarterly = fields.Float(compute='_kra_final_score_compute', string='This quarterly  final score', default=100, readonly='1')
    kra_final_score_last_quarterly = fields.Float(compute='_kra_final_score_compute', string='Last quarterly final score', default=100, readonly='1')
    kras = fields.One2many('employee.kra', 'employee_id', string="KRAS", help="KRAS", compute='_get_kras')
                          #domain=[('state', '=', 'done')])

    def _get_kras(self):
        months = []
        quarterlys = []
        this_month = datetime.now().month
        year = datetime.now().year
        months.append(this_month)

        if this_month == 1:
            last_month = 12
            year = year - 1
        else:
            last_month = this_month - 1
        months.append(last_month)

        this_quarterly = (this_month - 1)//3 + 1
        quarterlys.append(this_quarterly)
        if ((this_quarterly - 1)//3 - 1) == 0:
            last_quarterly = 1
            quarterlys.append(last_quarterly)
        else:
            last_quarterly = (this_quarterly - 1)//3 - 1
            quarterlys.append(last_quarterly)
        for rec in self:

            kra = self.env['employee.kra'].search([('employee_id', '=', rec.id), ('state', '=', 'done'), ('year', '=', str(year)), ('name', 'in', months)])
            rec.kras = kra



    def _kra_final_score_compute(self):
        this_month = datetime.now().month
        year = datetime.now().year
        months = [3, 6, 9, 12]
        if this_month == 1:
            last_month = 12
            year = year - 1
        else:
            last_month = this_month - 1

        this_quarterly = (this_month - 1) // 3 + 1
        if ((this_quarterly - 1)//3 - 1) == 0:
            last_quarterly = 1

        else:
            last_quarterly = (this_quarterly - 1)//3 - 1


        for emp in self:
            final_score_this_month = 0
            final_score_last_month = 0
            final_score_this_quarterly = 0
            final_score_last_quarterly = 0
            this_month_records = 0
            last_month_records = 0
            this_quarterly_records = 0
            last_quarterly_records = 0

            for kra_id in emp.kras:

                questions = self.env['employee.kra.question'].search([('employee_kra_id', '=', kra_id.id)])

                for question in questions:
                    if kra_id.name == str(this_month) and kra_id.year.name == str(year) :

                        if this_month in months and kra_id.quarterly == str(this_quarterly):
                            this_quarterly_records += 1
                            final_score_this_quarterly = final_score_this_quarterly + question.final_score
                        else:
                            this_month_records += 1
                            final_score_this_month = final_score_this_month + question.final_score

                    elif last_month in months and kra_id.quarterly == str(last_quarterly):
                        last_quarterly_records += 1
                        final_score_last_quarterly = final_score_last_quarterly + question.final_score
                    else:
                        last_month_records += 1
                        final_score_last_month = final_score_last_month + question.final_score

            if last_month_records == 0:
                last_month_records = 1
            if this_month_records == 0:
                this_month_records = 1
            if last_quarterly_records == 0:
                last_quarterly_records = 1
            if this_quarterly_records == 0:
                this_quarterly_records = 1

            emp.kra_final_score_last_month = final_score_last_month / last_month_records
            emp.kra_final_score_this_month = final_score_this_month / this_month_records
            emp.kra_final_score_last_quarterly = final_score_last_quarterly / last_quarterly_records
            emp.kra_final_score_this_quarterly = final_score_this_quarterly / this_quarterly_records


