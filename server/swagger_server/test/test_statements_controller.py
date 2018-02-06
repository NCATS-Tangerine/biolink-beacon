# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.statement import Statement  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStatementsController(BaseTestCase):
    """StatementsController integration test stubs"""

    def test_get_statements(self):
        """Test case for get_statements

        
        """
        query_string = [('s', 's_example'),
                        ('relations', 'relations_example'),
                        ('t', 't_example'),
                        ('keywords', 'keywords_example'),
                        ('semanticGroups', 'semanticGroups_example'),
                        ('pageNumber', 56),
                        ('pageSize', 56)]
        response = self.client.open(
            '//statements',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
