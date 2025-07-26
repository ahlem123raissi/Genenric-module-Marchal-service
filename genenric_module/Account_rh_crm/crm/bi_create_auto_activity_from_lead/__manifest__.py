# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name": "Auto Activity Creation from Lead | Lead Based Auto Activity | Schedule Activity for CRM Leads",
    "version": "18.0.0.0",
    "category": "CRM",
    "summary": "auto create activity from lead generate activity from lead follow up from lead create activity from crm lead generate crm activity auto create lead to crm activity instant activity on lead website to crm activity website lead to crm activity ",
    "description": """ Auto Activity Creation from Lead automates the scheduling of follow-up activities in Odoo CRM whenever a new lead is generated—especially from website inquiries like “Contact Us” forms. This module automatically creates and assigns predefined activities such as calls, emails, or meetings to the responsible user without any manual effort. With configurable settings, you can choose the activity type, assign the responsible salesperson, and set due dates to ensure timely follow-ups. As soon as a lead is created, the related activity is scheduled in real time, helping sales teams respond promptly and never miss important opportunities. """,
    "author": "BROWSEINFO",
    'website': "https://www.browseinfo.com/demo-request?app=bi_create_auto_activity_from_lead&version=18&edition=Community",
    'depends': ['base','website','crm'],
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
    "auto_install": False,
    'license': 'OPL-1',
    'live_test_url': 'https://www.browseinfo.com/demo-request?app=bi_create_auto_activity_from_lead&version=18&edition=Community',
    "images": ['static/description/Banner.gif'],
}
