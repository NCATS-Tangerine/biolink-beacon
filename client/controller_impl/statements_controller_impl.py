from swagger_server.models.beacon_statement import BeaconStatement
from swagger_server.models.beacon_statement_object import BeaconStatementObject
from swagger_server.models.beacon_statement_subject import BeaconStatementSubject
from swagger_server.models.beacon_statement_predicate import BeaconStatementPredicate

from ontobio.golr.beacon_query import BeaconAssociationQuery

from controller_impl import utils

def get_statements(s, edge_label=None, relation=None, t=None, keywords=None, categories=None, size=None):
    size = utils.sanitize_int(size, 5)

    if categories is not None:
        categories = [utils.map_category(t) for t in categories]

    relations = [edge_label, relation]
    relations = [r for r in relations if r is not None]

    g = BeaconAssociationQuery(
    	sources=s,
        targets=t,
    	keywords=keywords,
        categories=categories,
    	relations=relations,
        rows=size
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

        subject_categories = _subject['category']
        object_categories = _object['category']

        if isinstance(subject_categories, list):
            subject_categories = [utils.map_category(c) for c in subject_categories]
        else:
            subject_categories = [subject_categories]

        if isinstance(object_categories, list):
            object_categories = [utils.map_category(c) for c in object_categories]
        else:
            object_categories = [object_categories]

        statement_subject = BeaconStatementSubject(
            id=_subject['id'],
            name=_subject['label'],
            categories=subject_categories
        )

        statement_object = BeaconStatementObject(
            id=_object['id'],
            name=_object['label'],
            categories=object_categories
        )

        edge_label = '_'.join(_relation['label'].split())

        statement_predicate = BeaconStatementPredicate(
            relation=_relation['id'],
            edge_label=edge_label
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
