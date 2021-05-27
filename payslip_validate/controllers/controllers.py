# -*- coding: utf-8 -*-
# from odoo import http


# class PayslipValidate(http.Controller):
#     @http.route('/payslip_validate/payslip_validate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payslip_validate/payslip_validate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payslip_validate.listing', {
#             'root': '/payslip_validate/payslip_validate',
#             'objects': http.request.env['payslip_validate.payslip_validate'].search([]),
#         })

#     @http.route('/payslip_validate/payslip_validate/objects/<model("payslip_validate.payslip_validate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payslip_validate.object', {
#             'object': obj
#         })
