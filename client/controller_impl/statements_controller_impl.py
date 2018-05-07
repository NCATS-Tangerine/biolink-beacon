from swagger_server.models.beacon_statement import BeaconStatement
from swagger_server.models.beacon_statement_object import BeaconStatementObject
from swagger_server.models.beacon_statement_subject import BeaconStatementSubject
from swagger_server.models.beacon_statement_predicate import BeaconStatementPredicate

from ontobio.golr.beacon_query import BeaconAssociationQuery

from controller_impl import utils

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
    :param types: a (url-encoded, space-delimited) string of semantic groups (specified as codes CHEM, GENE, ANAT, etc.) to which to constrain the subject or object concepts associated with the query seed concept (see [Semantic Groups](https://metamap.nlm.nih.gov/Docs/SemGroups_2013.txt) for the full list of codes)
    :type types: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of concepts per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[Statement]
    """
    pageNumber = utils.sanitize_int(pageNumber)
    pageSize = utils.sanitize_int(pageSize, 5)

    if types is not None:
        types = [utils.map_category(t) for t in types]

    g = BeaconAssociationQuery(
    	sources=s,
        targets=t,
    	keywords=keywords,
        categories=types,
    	relations=relations,
        start=pageNumber,
        rows=pageSize
    )

    results = utils.try_multi(method=g.exec)

    associations = results['associations']

    statements = []

    for d in associations:
        _subject = d['subject']
        _object = d['object']
        _relation = d['relation']

        if _subject is None or _object is None or _relation is None:
            continue

        subject_categories = _subject['categories']
        object_categories = _object['categories']

        if isinstance(subject_categories, list):
            subject_categories = [utils.map_category(c) for c in subject_categories]

        if isinstance(object_categories, list):
            object_categories = [utils.map_category(c) for c in object_categories]

        statement_subject = BeaconStatementSubject(
            id=_subject['id'],
            name=_subject['label'],
            type=', '.join(subject_categories)
        )

        statement_object = BeaconStatementObject(
            id=_object['id'],
            name=_object['label'],
            type=', '.join(object_categories)
        )

        statement_predicate = BeaconStatementPredicate(
            id=_relation['id'],
            name=_relation['label']
        )

        identifier = d['id']

        if ':' not in identifier:
            identifier = utils.biolink_prefix() + ':' + identifier

        statement = BeaconStatement(
            id=identifier,
            subject=statement_subject,
            predicate=statement_predicate,
            object=statement_object
        )

        statements.append(statement)

    return statements
