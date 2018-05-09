import connexion
import six

from swagger_server.models.beacon_annotation import BeaconAnnotation  # noqa: E501
from swagger_server.models.beacon_statement import BeaconStatement  # noqa: E501
from swagger_server import util

import controller_impl as ctrl

def get_evidence(statementId, keywords=None, size=None):  # noqa: E501
    """get_evidence

    Retrieves a (paged) list of annotations cited as evidence for a specified concept-relationship statement  # noqa: E501

    :param statementId: (url-encoded) CURIE identifier of the concept-relationship statement (\&quot;assertion\&quot;, \&quot;claim\&quot;) for which associated evidence is sought
    :type statementId: str
    :param keywords: an array of keywords or substrings against which to filter citation titles
    :type keywords: List[str]
    :param size: maximum number of cited references requested by the query (default 100)
    :type size: int

    :rtype: List[BeaconAnnotation]
    """
    return ctrl.get_evidence(statementId, keywords, size)


def get_statements(s, relations=None, t=None, keywords=None, categories=None, size=None):  # noqa: E501
    """get_statements

    Given a specified set of [CURIE-encoded](https://www.w3.org/TR/curie/)  &#39;source&#39; (&#39;s&#39;) concept identifiers,  retrieves a paged list of relationship statements where either the subject or object concept matches any of the input &#39;source&#39; concepts provided.  Optionally, a set of &#39;target&#39; (&#39;t&#39;) concept  identifiers may also be given, in which case a member of the &#39;target&#39; identifier set should match the concept opposing the &#39;source&#39; in the  statement, that is, if the&#39;source&#39; matches a subject, then the  &#39;target&#39; should match the object of a given statement (or vice versa).  # noqa: E501

    :param s: an array set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of  &#39;source&#39; concepts possibly known to the beacon. Unknown CURIES should simply be ignored (silent match failure).
    :type s: List[str]
    :param relations: an array set of strings of Biolink predicate relation name labels against which to constrain the search for statement relations associated with the given query seed concept. The predicate  relation names for this parameter should be as published by  the beacon-aggregator by the /predicates API endpoint as taken from the minimal predicate list of the Biolink Model  (see [Biolink Model](https://biolink.github.io/biolink-model)  for the full list of predicates).
    :type relations: List[str]
    :param t: (optional) an array set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of &#39;target&#39; concepts possibly known to the beacon.  Unknown CURIEs should simply be ignored (silent match failure).
    :type t: List[str]
    :param keywords: an array of keywords or substrings against which to filter concept names and synonyms
    :type keywords: List[str]
    :param categories: an array set of concept categories (specified as Biolink name labels codes gene, pathway, etc.) to which to constrain concepts matched by the main keyword search (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)
    :type categories: List[str]
    :param size: maximum number of statement entries requested by the query (default 100)
    :type size: int

    :rtype: List[BeaconStatement]
    """
    return ctrl.get_statements(s, relations, t, keywords, categories, size)
