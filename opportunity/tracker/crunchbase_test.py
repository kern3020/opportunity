'''

The crunchbase API is used to populate the company template if data is
available. Here are the tests.

python -m unittest crunchbase_test.FetchFromCrunch.test_normal

'''

from django.utils import unittest

import crunchbase


class FetchFromCrunch(unittest.TestCase):
    def test_normal(self):
        '''
        The simpliest case is a single token with no special characters
        which matches a specific company in crunchbase.
        '''
        proxy = crunchbase.CrunchProxy()
        proxy.query("Syapse")
        self.assertEqual(proxy.city, "Palo Alto")

    def test_encoding(self):
        '''
        What happens if the string needs to be encode?
        '''
        proxy = crunchbase.CrunchProxy()
        proxy.query("Pacific Biosciences")
        self.assertEqual(proxy.city, "Menlo Park")

    def test_matches_multiple(self):
        '''
        What happens if a company has multiple offices?
        '''
        proxy = crunchbase.CrunchProxy()
        proxy.query("IBM")
        self.assertEqual(proxy.city, "Armonk")

    def test_no_match(self):
        '''
        What happens if there is no match with crunchbase?
        '''
        name = '9329eb13-912c-4336-8c35-903ebc84f971'
        proxy = crunchbase.CrunchProxy()
        proxy.query(name)
        self.assertEqual(proxy.name, None)
        self.assertEqual(proxy.city, None)
