# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestExactmatchesController(BaseTestCase):
    """ExactmatchesController integration test stubs"""

    def test_get_exact_matches_to_concept(self):
        """Test case for get_exact_matches_to_concept

        
        """
        response = self.client.open(
            '//exactmatches/{conceptId}'.format(conceptId='conceptId_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_exact_matches_to_concept_list(self):
        """Test case for get_exact_matches_to_concept_list

        
        """
        query_string = [('c', 'c_example')]
        response = self.client.open(
            '//exactmatches',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
