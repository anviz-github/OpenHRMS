# See LICENSE file for full copyright and licensing details.
from datetime import *
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrAcademic(models.Model):
    _name = 'hr.academic'
    _inherit = 'hr.curriculum'
    _description = 'Academic experiences'

    study_field = fields.Char(string='Field of study', translate=True, )
    activities = fields.Text(string='Activities and associations',
                             translate=True)

    @api.constrains('start_date', 'end_date')
    def validate_dates(self):
        if not self.env.context.get('website_id'):
            if self.end_date:
                today = date.today()
                for dates in self:
                    if dates.start_date > today:
                        raise ValidationError(_('Start date (%s) should be less than Current Date in Academic Experience') % dates.start_date)
                    if dates.end_date > today:
                        raise ValidationError(_('End date (%s) should be less than Current Date in Academic Experience') % dates.end_date)
                    if dates.start_date > dates.end_date:
                        raise ValidationError(_('End date (%s) should be greater than Start Date (%s) in Academic Experience') % dates.start_date, dates.end_date)

    def write(self, vals):
        if vals.get("is_still"):
            vals.update({'end_date': None})
        result = super(HrAcademic, self).write(vals)
        return result
