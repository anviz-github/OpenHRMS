# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InsurancePolicy(models.Model):
    _name = 'insurance.policy'

    name = fields.Char(string='Name', required=True, translate=True)
    company_percentage = fields.Float(string="Company Percentage ", help="Company insurance percentage")
    personal_percentage = fields.Float(string="Personal Percentage ", help="Personal insurance percentage")
    insure_type = fields.Selection([('SIA', 'Social Insurance Base'), ('HRA', 'House Rent Allowance Base')],
                                       required=True, default='SIA',
                                       string='Insurance Type', help="Insurance Type")
    note_field = fields.Html(string='Comment', help="Notes for the insurance policy if any")
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)
