# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    not_allow_marketing_mails = fields.Boolean(
        string="No permite emails de marketing"
    )                                                                                                     