# See LICENSE file for full copyright and licensing details.
from datetime import *
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrExperience(models.Model):
    _name = 'hr.experience'
    _inherit = 'hr.curriculum'

    notice_period = fields.Selection(
        [('s_notice_period', 'Serving Notice Period'),
         ('15days', '15 Days or less'), ('1month', '1 Month'),
         ('2months', '2 Months'), ('3months', '3 Months'),
         ('above3months', 'More than 3 Months')],
        default='')
    referee_name = fields.Char(string="Name of referee")
    referee_position = fields.Char(string="Position of referee")
    referee_contact = fields.Char(string="Contact details")
    type = fields.Selection(
        [('full_time', 'Full time'), ('part_time', 'Part time')], 'Work type',
        required=True,
        default='full_time', help='Define Work Type')

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
        result = super(HrExperience, self).write(vals)
        return result
