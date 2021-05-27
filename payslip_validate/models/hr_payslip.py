from odoo import models


class Payslip(models.Model):
    _name = "hr.payslip"
    _inherit = ["hr.payslip", "tier.validation", "mail.thread"]
    _state_from = ["draft", "verify", "to approve"]
    _state_to = ["done", "approved"]