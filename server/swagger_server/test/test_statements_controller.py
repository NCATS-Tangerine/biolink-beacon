# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.beacon_statement import BeaconStatement  # noqa: E501
from swagger_server.models.beacon_statement_with_details import BeaconStatementWithDetails  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStatementsController(BaseTestCase):
    """StatementsController integration test stubs"""

    def test_get_statement_details(self):
        """Test case for get_statement_details

        
        """
        query_string = [('keywords', 'keywords_example'),
                        ('size', 56)]
        response = self.client.open(
            '/beacon/biolink//statements/{statementId}'.format(statementId='statementId_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_statements(self):
        """Test case for get_statements

        
        """
        query_string = [('s', 's_example'),
                        ('edge_label', 'edge_label_example'),
                        ('relation', 'relation_example'),
                        ('t', 't_example'),
                        ('keywords', 'keywords_example'),
                        ('categories', 'categories_example'),
                        ('size', 56)]
        response = self.client.open(
            '/beacon/biolink//statements',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
