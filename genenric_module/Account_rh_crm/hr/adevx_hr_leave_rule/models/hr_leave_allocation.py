from odoo import api, models, fields, _
from odoo.exceptions import UserError


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    state = fields.Selection([
        ('confirm', 'To Approve'),
        ('validate', 'Approved'),
        ('refuse', 'Refused')],
        string='Status', readonly=True, tracking=True, copy=False, default='confirm',
        help="The status is set to 'To Submit', when an allocation request is created."
             "\nThe status is 'To Approve', when an allocation request is confirmed by user."
             "\nThe status is 'Refused', when an allocation request is refused by manager."
             "\nThe status is 'Approved', when an allocation request is approved by manager.")

    def action_draft(self):
        if any(holiday.state not in ['validate', 'refuse'] for holiday in self):
            raise UserError(
                _('Allocation request state must be "Refused" or "Approve" in order to be reset to draft.'))
        self.write({
            'state': 'confirm',
        })
        linked_requests = self.mapped('linked_request_ids')
        if linked_requests:
            linked_requests.action_draft()
            linked_requests.unlink()
        self.activity_update()
        return True

    @api.constrains('holiday_status_id', 'number_of_days_display', 'number_of_hours_display')
    def check_holiday_status_duration(self):
        for rec in self:
            # Get shared domain
            if rec.holiday_status_id.leave_rule_id:
                domain = [
                    ('id', '!=', rec.id),
                    ('employee_id', '=', rec.employee_id.id),
                    ('holiday_status_id.leave_rule_id', '=', rec.holiday_status_id.leave_rule_id.id)
                ]

                if rec.holiday_status_id.leave_rule_id.allocation_unit == 'hour':
                    old_hours = sum(self.search(domain).mapped('number_of_hours_display'))
                    total_hours = rec.number_of_hours_display + old_hours
                    limit_hours = rec.holiday_status_id.leave_rule_id.maximum_allocation
                    if total_hours != limit_hours:
                        raise UserError("Duration should be equal %s hours" % limit_hours)
                else:
                    old_days = sum(self.search(domain).mapped('number_of_days_display'))
                    total_days = rec.number_of_days_display + old_days
                    limit_days = rec.holiday_status_id.leave_rule_id.maximum_allocation
                    if total_days != limit_days:
                        raise UserError("Duration should be equal %s days" % limit_days)
