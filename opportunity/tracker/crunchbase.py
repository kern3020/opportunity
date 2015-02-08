'''
CrunchBase allows access to there database of technology companies,
people, and investors. This is a proxy for the Crunchbase API.  This
is good for people looking for jobs in technology. Keep an eye open
for other data sources for different disciplines.

'''

import os
import json
import logging

# Using python 3 specific APIs
from http.client import responses
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen


class CrunchProxy():
    '''
    This class does the heavy lifting. The view shouldn't know about the keys
    in the json returned by the cruncbase API.
    '''
    def __init__(self):
        self.base_url = "http://api.crunchbase.com/v/2"
        self.api_key = os.environ['CRUNCHBASE_KEY']
        self.co_request_template = "{0}/{1}?user_key={2}"
        self.generic_request_template = "{0}/organizations?name={1}&organization_types=company&user_key={2}&page=1"

        # results
        self._name = None
        self._description = None
        self._street_address = None
        self._city = None
        self._state = None
        self._zip = None
        self._country = None
        self._website = None

    def __str__(self):
        return "{0}\n{1}, {2}\n{3}".format(
            self._name, self._city, self._state, self._description)

    @property
    def name(self):
        return self._name

    @property
    def street_address(self):
        return self._street_address

    @property
    def city(self):
        return self._city

    @property
    def state(self):
        return self._state

    @property
    def zip(self):
        return self._zip

    @property
    def website(self):
        return self._website

    def query(self, query):
        results = {}
        try:
            # see if we can find the exact name as name of org
            url_request = self.generic_request_template.format(
                self.base_url, quote(query), self.api_key)
            results = json.loads(urlopen(url_request).readall().decode("utf-8"))
            if len(results['data']['items']) == 0:
                self.log_protocol_err('{0} - no matches found'.format(query))
            else:
                # on success, retrieve path to and submit query
                path = results['data']['items'][0]['path']  # assumption first record is best.
                url_request = self.co_request_template.format(
                    self.base_url, quote(path),
                    self.api_key)
                results = json.loads(urlopen(url_request).readall().decode("utf-8"))
                if 'response' in results['data'] and results['data']['response'] is False:
                    self.log_protocol_err(results['data']['error'])
                else:
                    self._name = results['data']['properties']['name']
                    self._description = results['data']['properties']['description']
                    self._website = results['data']['properties']['homepage_url']
                    list_of_offices = results['data']['relationships']['offices']['items']
                    zz = list_of_offices
                    if len(list_of_offices) > 0:
                        office = list_of_offices[0]
                        self._street_address = ""
                        if office['street_1']:
                            self._street_address += office['street_1']
                        if office['street_2']:
                            self._street_address += office['street_2']
                        self._city = office['city']
                        self._state = office['region']
                        self._country = office['country']
                        self._zip = office['postal_code']
        except HTTPError as e:
            logging.error(str.format("HTTP Error: {0} - {1}", e.code,
                                     responses[e.code]))

    def log_protocol_err(self, msg):
        logging.error(msg)
