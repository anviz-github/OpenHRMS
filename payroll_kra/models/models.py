# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class payroll_kra(models.Model):
#     _name = 'payroll_kra.payroll_kra'
#     _description = 'payroll_kra.payroll_kra'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100