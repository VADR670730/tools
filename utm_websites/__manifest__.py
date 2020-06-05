# -*- coding: utf-8 -*-
{
    'name': 'Utm websites',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/utm_website_view.xml',
    ],
    'installable': True,
    'auto_install': False,    
}