# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.summary import Summary  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSummaryController(BaseTestCase):
    """SummaryController integration test stubs"""

    def test_linked_types(self):
        """Test case for linked_types

        
        """
        response = self.client.open(
            '//types',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
