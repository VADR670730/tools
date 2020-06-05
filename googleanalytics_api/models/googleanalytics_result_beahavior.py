# -*- coding: utf-8 -*-
from odoo import api, fields, models
import odoo

from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

from .googleanalytics_webservice import GoogleanalyticsWebservice

class GoogleanalyticsResultBeahavior(models.Model):
    _name = 'googleanalytics.result.beahavior'
    _description = 'Googleanalytics Result Beahavior'
    
    landingPagePath = fields.Char(        
        string='landingPagePath'
    )
    sessionDuration = fields.Float(        
        string='sessionDuration'
    )
    pageviews = fields.Integer(        
        string='pageviews'
    )
    exits = fields.Integer(        
        string='exits'
    )
    sessions = fields.Integer(        
        string='sessions'
    )
    webPropertyId = fields.Char(        
        string='webPropertyId'
    )
    pagePath = fields.Char(        
        string='pagePath'
    )
    eventCategory = fields.Char(        
        string='eventCategory'
    )
    totalEvents = fields.Integer(        
        string='totalEvents'
    )
    eventAction = fields.Char(        
        string='eventAction'
    )
    userType = fields.Char(        
        string='userType'
    )
    bounceRate = fields.Float(        
        string='bounceRate'
    )
    entrances = fields.Integer(        
        string='entrances'
    )
    profileName = fields.Char(        
        string='profileName'
    )
    date = fields.Date(        
        string='date'
    )
    profileId = fields.Char(        
        string='profileId'
    )
    users = fields.Integer(        
        string='users'
    )
    timeOnPage = fields.Float(        
        string='timeOnPage'
    )
    uniqueEvents = fields.Integer(        
        string='uniqueEvents'
    )
    accountId = fields.Integer(        
        string='accountId'
    )

    @api.model
    def get_day_info(self, date, profile_id):
        _logger.info(date)
        _logger.info(profile_id)
        # GoogleanalyticsWebservice
        key_file_location = odoo.tools.config.get('googleanalytics_api_key_file')
        googleanalytics_webservice = GoogleanalyticsWebservice(key_file_location)
        #define
        metrics = ['ga:users', 'ga:sessions', 'ga:sessionDuration', 'ga:bounceRate', 'ga:pageviews', 'ga:timeOnPage', 'ga:totalEvents', 'ga:uniqueEvents', 'ga:entrances', 'ga:exits']
        dimensions = ['ga:date', 'ga:userType', 'ga:landingPagePath', 'ga:pagePath', 'ga:eventCategory', 'ga:eventAction', 'ga:eventLabel']
        # search
        googleanalytics_result_beahavior_ids = self.env['googleanalytics.result.beahavior'].sudo().search([('date', '=', str(date)), ('profileId', '=', str(profile_id))])
        if len(googleanalytics_result_beahavior_ids) == 0:
            results = googleanalytics_webservice.get_results(profile_id, date, date, metrics, dimensions)
            if 'rows' in results:
                if len(results['rows']) > 0:
                    for row in results['rows']:
                        count = 0
                        # vals
                        googleanalytics_result_beahavior_vals = {
                            'webPropertyId': str(results['profileInfo']['webPropertyId']),
                            'profileId': str(results['profileInfo']['profileId']),
                            'profileName': str(results['profileInfo']['profileName']),
                            'accountId': str(results['profileInfo']['accountId'])
                        }
                        for columnHeader in results['columnHeaders']:
                            # row_value
                            row_value = str(row[count])
                            # data
                            columnHeaderName = str(columnHeader['name'])
                            columnHeaderName = columnHeaderName.replace('ga:', '')

                            columnHeaderDataType = str(columnHeader['dataType'])
                            # pre_item
                            googleanalytics_result_beahavior_vals[columnHeaderName] = ''
                            # fix
                            if row_value == '(none)' or row_value == '(not set)':
                                row_value = ''
                            # ga:source
                            if columnHeaderName == 'source':
                                row_value = row_value.replace('(', '').replace(')', '')
                            # ga:date
                            if columnHeaderName == 'date':
                                new_row_value = str(row_value[0:4]) + '-' + str(row_value[4:6]) + '-' + str(row_value[6:8])
                                row_value = new_row_value
                            # types
                            if columnHeaderDataType == 'INTEGER':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = int(row_value)
                            elif columnHeaderDataType == 'STRING':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = str(row_value)
                            elif columnHeaderDataType == 'PERCENT':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = row_value
                            elif columnHeaderDataType == 'TIME':
                                googleanalytics_result_beahavior_vals[columnHeaderName] = row_value
                            # count
                            count += 1
                        # remove eventLabel
                        if 'eventLabel' in googleanalytics_result_beahavior_vals:
                            del googleanalytics_result_beahavior_vals['eventLabel']
                        # add_item
                        googleanalytics_result_beahavior_obj = self.env['googleanalytics.result.beahavior'].sudo().create(googleanalytics_result_beahavior_vals)

    @api.model
    def cron_get_yesterday_info(self):
        _logger.info('cron_get_yesterday_info')
        #vars
        profile_ids = str(self.env['ir.config_parameter'].sudo().get_param('googleanalytics_api_profile_ids')).split(',')
        current_date = datetime.today()
        date_yesterday = current_date + relativedelta(days=-1)
        #config
        for profile_id in profile_ids:
            self.get_day_info(date_yesterday.strftime("%Y-%m-%d"), profile_id)

    @api.model
    def cron_get_all_year_info(self):
        _logger.info('cron_get_all_year_info')
        # vars
        profile_ids = str(self.env['ir.config_parameter'].sudo().get_param('googleanalytics_api_profile_ids')).split(',')
        end_date = datetime.today()
        start_date = datetime(end_date.year, 1, 1)
        date_item = start_date
        #operations
        while date_item.strftime("%Y-%m-%d")!=end_date.strftime("%Y-%m-%d"):
            for profile_id in profile_ids:
                self.get_day_info(date_item.strftime("%Y-%m-%d"), profile_id)
            #increase
            date_item = date_item + relativedelta(days=1)