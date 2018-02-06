# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.annotation import Annotation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEvidenceController(BaseTestCase):
    """EvidenceController integration test stubs"""

    def test_get_evidence(self):
        """Test case for get_evidence

        
        """
        query_string = [('keywords', 'keywords_example'),
                        ('pageNumber', 56),
                        ('pageSize', 56)]
        response = self.client.open(
            '//evidence/{statementId}'.format(statementId='statementId_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
