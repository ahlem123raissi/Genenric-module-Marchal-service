from odoo import api, fields, models


class HrLeaveRule(models.Model):
    _name = 'hr.leave.rule'
    _rec_name = 'name'
    _description = 'HR Leave Rule'

    name = fields.Char(string="Name", required=True)
    maximum_allocation = fields.Float(string="Maximum Allocation", required=True)
    allocation_unit = fields.Selection(string="Allocation Unit", selection=[
        ('hour', 'Hours'), ('day', 'Days')], required=True)

    time_off_request_rule = fields.Boolean(
        string="Time Off Request Rule", help="this Field to prevent employee to allocate Time off in previous periods")
    time_off_request_before = fields.Float(string="Time Off Request Must Be Before")
    maximum_time_off_each_request = fields.Float(string="Maximum Time Off For Each Request")

    start_time_off_allocation = fields.Boolean(
        string="Start Time-off Allocation",
        help="Allow employee To request time off after (Start Time-off Allocation After) from employee first contract date ")

    start_time_off_allocation_after = fields.Float(string="Start Time-off Allocation After")
