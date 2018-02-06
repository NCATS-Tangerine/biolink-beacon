import connexion
import six

from swagger_server.models.annotation import Annotation  # noqa: E501
from swagger_server import util


def get_evidence(statementId, keywords=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_evidence

    Retrieves a (paged) list of annotations cited as evidence for a specified concept-relationship statement  # noqa: E501

    :param statementId: (url-encoded) CURIE identifier of the concept-relationship statement (\&quot;assertion\&quot;, \&quot;claim\&quot;) for which associated evidence is sought 
    :type statementId: str
    :param keywords: (url-encoded, space delimited) keyword filter to apply against the label field of the annotation 
    :type keywords: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results 
    :type pageNumber: int
    :param pageSize: number of cited references per page to be returned in a paged set of query results 
    :type pageSize: int

    :rtype: List[Annotation]
    """
    return 'do some magic!'
