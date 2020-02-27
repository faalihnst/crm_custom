# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil import relativedelta


class crm_edit(models.Model):
    _inherit = "crm.lead"

    self_archive = fields.Boolean(string='Automatic Archive')
    days_archive = fields.Integer(string='Days to Archive')

    @api.multi
    def make_lead_inactive(self):
        today = date.today()
        datetime_format = "% Y-% m-% d% H:% M:% S"
        from_dt = datetime.strptime(today, datetime_format)
        to_dt = datetime.strptime(self.create_date, datetime_format)
        timedelta = to_dt - from_dt
        diff_day = timedelta.days + float (timedelta.seconds) / 86400
        for record in self:
            if record.self_archive == True and diff_day > record.days_archive:
                record.active = False

    @api.model
    def fields_get(self, fields=None):
        fields_to_hide = ['active']
        res = super(crm_edit, self) .fields_get()
        has_my_group = self.env.user.has_group('crm_custom.group_crm_leads_archive')
        for field in fields_to_hide:
            if not has_my_group:
                res[field]['selectable'] = False
            else:
                res[field]['selectable'] = True
        return res
