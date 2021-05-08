# -*- coding: utf-8 -*-
# from odoo import http


# class PayrollKra(http.Controller):
#     @http.route('/payroll_kra/payroll_kra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payroll_kra/payroll_kra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payroll_kra.listing', {
#             'root': '/payroll_kra/payroll_kra',
#             'objects': http.request.env['payroll_kra.payroll_kra'].search([]),
#         })

#     @http.route('/payroll_kra/payroll_kra/objects/<model("payroll_kra.payroll_kra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payroll_kra.object', {
#             'object': obj
#         })
