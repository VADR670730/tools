# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CescePaymentTerm(models.Model):
    _name = 'cesce.payment.term'
    _description = 'Cesce Payment Term'    
    
    code = fields.Char(        
        string='Codigo'
    )
    name = fields.Char(        
        string='Nombre'
    )                                       