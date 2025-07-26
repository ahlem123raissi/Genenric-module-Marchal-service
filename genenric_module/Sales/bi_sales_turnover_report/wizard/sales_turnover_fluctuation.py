# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import datetime
import pandas as pd


class SalesTurnoverFluctuation(models.TransientModel):
    _name = 'sales.turnover.fluctuation'
    _description = "Sales Turnover Fluctuation Record"


    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    discrepancy = fields.Integer('Discrepancy%')
    turnover_limit = fields.Float('Monthly Turnover Limit')
    calculation_type = fields.Selection([('taxed','Taxed'),('without_taxed','Without Taxed')],string="Calculation Type")
    include_invoice_draft = fields.Boolean('Include Invoice Draft')
    partner_ids = fields.Many2many('res.partner','res_partner_rel','partner_id','res_id',string="Customer")



    def create_report(self):
        active_ids = self._context.get('active_ids', False)
        data = {
            'active_ids' : active_ids, 
            'start_date' : self.start_date, 
            'end_date' : self.end_date,
            'discrepancy' : self.discrepancy,
            'turnover_limit' : self.turnover_limit,
            'calculation_type' : self.calculation_type,
            'include_invoice_draft' : self.include_invoice_draft,
            'partner_ids' : self.partner_ids.ids,
        }   
        return self.env.ref('bi_sales_turnover_report.report_sales_turnover').report_action(self.id, data=data)


    
class ReportSalesTurnover(models.AbstractModel):
    _name = 'report.bi_sales_turnover_report.sales_turnover_invoice'
    _description = "Sales Turnover Fluctuation Report"


    
    @api.model
    def _get_report_values(self, docids, data=None):
        start_date, end_date = data.get('start_date'), data.get('end_date')
        dtrange = pd.date_range(start=start_date, end=end_date, freq='d')
        months = pd.Series(dtrange .month)
        starts, ends = months.ne(months.shift(1)), months.ne(months.shift(-1))
        df = pd.DataFrame({'month_starting_date': dtrange[starts].strftime('%Y-%m-%d'),
                   'month_ending_date': dtrange[ends].strftime('%Y-%m-%d')})
        date_ranges = df.values.tolist()
        domain = [('date_order','>=',data.get('start_date')),('date_order','<=',data.get('end_date'))]
        if not data.get("include_invoice_draft"):
            domain += [('invoice_ids.state','in',['posted'])]
        order_ids = self.env['sale.order'].search(domain)    
        if data.get("partner_ids"):
            partner_ids = self.env['res.partner'].browse(data.get("partner_ids"))
        else:
            partner_ids = order_ids.mapped("partner_id")
        vals = {}
        to_be_delete = []
        for partner_id in partner_ids:
            if not partner_id in vals.keys():
                vals[partner_id] = {}
            for date_range in date_ranges:
                domain = [('date_order','>=',date_range[0]),('date_order','<=',date_range[1]),('partner_id','=',partner_id.id)]
                if not data.get("include_invoice_draft"):
                    domain += [('invoice_ids.state','in',['posted'])]
                order_id = self.env['sale.order'].search(domain)
                if data.get('calculation_type') == 'taxed':
                    current_total = sum(sale_id.amount_total for sale_id in order_id)
                else:
                    current_total = sum(sale_id.amount_untaxed for sale_id in order_id)
                if data.get('turnover_limit'):
                    if data.get('turnover_limit') == current_total:
                        to_be_delete.append(partner_id)
                date_range_index = date_ranges.index(date_range)
                discrepancy = 0
                if date_range_index :
                    previous_index = date_range_index - 1
                    last_month_date_range = date_ranges[previous_index]
                    sale_domain = [('partner_id','=',partner_id.id),('date_order','>=',last_month_date_range[0]),('date_order','<=',last_month_date_range[1])]
                    if not data.get("include_invoice_draft"):
                        sale_domain += [('invoice_ids.state','in',['posted'])]
                    sales_id = self.env['sale.order'].search(sale_domain)
                    if data.get('calculation_type') == 'taxed':
                        previous_total = sum(sale_ids.amount_total for sale_ids in sales_id)
                    else:
                        previous_total = sum(sale_ids.amount_untaxed for sale_ids in sales_id)
                    discrepancy = ((((current_total - previous_total) / previous_total) * 100)) if previous_total else 0.0
                    if data.get('discrepancy'):
                        if data.get('discrepancy') == discrepancy:
                            to_be_delete.append(partner_id)   
                vals[partner_id].update({date_range[0]:[current_total,discrepancy]}) 
        to_be_delete = list(set(to_be_delete))
        for delete_partner in to_be_delete:
            del vals[delete_partner]
        return{
            'date_ranges' : date_ranges,
            'partner_ids' : partner_ids,
            'data' : data,
            'doc_ids' : docids,
            'report_datas':vals
        }