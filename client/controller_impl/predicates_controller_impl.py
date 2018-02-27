from ontobio.golr.golr_query import GolrAssociationQuery, M
from swagger_server.models.beacon_predicate import BeaconPredicate

def get_predicates():
	"""get_predicates

	Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


	:rtype: List[Predicate]
	"""

	g = GolrAssociationQuery(
		q='*:*',
		facet_fields=[M.RELATION, M.RELATION_LABEL],
		facet_pivot_fields=[M.RELATION, M.RELATION_LABEL],
		rows=0
	)

	results = g.exec()
	facet_pivot = results['facet_pivot']

	predicates = []

	for p in facet_pivot['relation,relation_label']:
		identifier = p['value']
		for pivot in p['pivot']:
			# not currently used
			count = pivot['count']
			name = pivot['value']
			predicate = BeaconPredicate(id=identifier, name=name, definition=None)
			predicates.append(predicate)

	return predicates
