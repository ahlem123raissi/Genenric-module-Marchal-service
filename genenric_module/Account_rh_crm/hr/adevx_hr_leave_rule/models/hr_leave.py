from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('employee_id', 'holiday_status_id', 'request_date_from')
    def check_holiday_status_date_from(self):
        for rec in self:
            current_date = fields.Date.today()
            if rec.holiday_status_id.leave_rule_id.time_off_request_rule:
                if rec.request_date_from:
                    target_start_date = current_date + timedelta(
                        days=rec.holiday_status_id.leave_rule_id.time_off_request_before)
                    if rec.request_date_from < target_start_date:
                        raise UserError("Start date should be greater than %s" % target_start_date)

            if rec.holiday_status_id.leave_rule_id.maximum_time_off_each_request:
                start_date = datetime.combine(current_date, datetime.min.time())
                end_date = datetime.combine(current_date, datetime.max.time())
                leave_ids = self.search([
                    ('holiday_status_id', '=', rec.holiday_status_id.id),
                    ('create_date', '>=', start_date),
                    ('create_date', '<=', end_date),
                    ('employee_id', '=', rec.employee_id.id),
                ])
                old_requests_per_day = sum(leave_ids.mapped('number_of_days'))
                total_requests_per_day = old_requests_per_day + rec.number_of_days
                if total_requests_per_day > rec.holiday_status_id.leave_rule_id.maximum_time_off_each_request:
                    raise UserError("Maximum days allowed for this day %s is: %s"
                                    % (current_date, rec.holiday_status_id.leave_rule_id.maximum_time_off_each_request))

            if rec.holiday_status_id.leave_rule_id.start_time_off_allocation:
                contract_date = rec.employee_id.contract_id.first_contract_date
                diff = relativedelta(current_date, contract_date)

                num_of_months = 0
                if diff.years:
                    num_of_months += diff.years * 12
                elif diff.months:
                    num_of_months += diff.months

                if num_of_months < rec.holiday_status_id.leave_rule_id.start_time_off_allocation_after:
                    raise UserError(
                        "To request time off for employee %s \n contract date should be greater than %s months"
                        % (self.employee_id.name, rec.holiday_status_id.leave_rule_id.start_time_off_allocation_after))
