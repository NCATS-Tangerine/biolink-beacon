import connexion
import six

from swagger_server.models.beacon_annotation import BeaconAnnotation  # noqa: E501
from swagger_server.models.beacon_statement import BeaconStatement  # noqa: E501
from swagger_server import util

import controller_impl

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

    :rtype: List[BeaconAnnotation]
    """
    return controller_impl.get_evidence(statementId, keywords, pageNumber, pageSize)


def get_statements(s, relations=None, t=None, keywords=None, types=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_statements

    Given a specified set of [CURIE-encoded](https://www.w3.org/TR/curie/) &#39;source&#39; (&#39;s&#39;) concept identifiers,  retrieves a paged list of relationship statements where either the subject or object concept matches any of the input &#39;source&#39; concepts provided.  Optionally, a set of &#39;target&#39; (&#39;t&#39;) concept  identifiers may also be given, in which case a member of the &#39;target&#39; identifier set should match the concept opposing the &#39;source&#39; in the  statement, that is, if the&#39;source&#39; matches a subject, then the  &#39;target&#39; should match the object of a given statement (or vice versa).  # noqa: E501

    :param s: a set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of  &#39;source&#39; concepts possibly known to the beacon. Unknown CURIES should simply be ignored (silent match failure).
    :type s: List[str]
    :param relations: a (url-encoded, space-delimited) string of predicate relation identifiers with which to constrain the statement relations retrieved  for the given query seed concept. The predicate ids sent should  be as published by the beacon-aggregator by the /predicates API endpoint.
    :type relations: str
    :param t: (optional) an array set of [CURIE-encoded](https://www.w3.org/TR/curie/)  identifiers of &#39;target&#39; concepts possibly known to the beacon.  Unknown CURIEs should simply be ignored (silent match failure).
    :type t: List[str]
    :param keywords: a (url-encoded, space-delimited) string of keywords or substrings against which to match the subject, predicate or object names of the set of concept-relations matched by any of the input exact matching concepts
    :type keywords: str
    :param types: a (url-encoded, space-delimited) string of concept types (specified as codes gene, pathway, etc.) to which to constrain the subject or object concepts associated with the query seed concept (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)
    :type types: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of concepts per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[BeaconStatement]
    """
    return controller_impl.get_statements(s, relations, t, keywords, types, pageNumber, pageSize)
