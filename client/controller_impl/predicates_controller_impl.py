from ontobio.golr.golr_query import GolrAssociationQuery, M
from swagger_server.models.beacon_predicate import BeaconPredicate

from cachetools.func import ttl_cache

from controller_impl import utils

__time_to_live_in_seconds = 604800

@ttl_cache(maxsize=500, ttl=__time_to_live_in_seconds)
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

	results = utils.try_multi(g.exec)

	facet_pivot = results['facet_pivot']

	predicates = []

	for p in facet_pivot['relation,relation_label']:
		identifier = p['value']
		for pivot in p['pivot']:
			name = pivot['value']
			count = pivot['count']

			edge_label = utils.snake_case(name)

			p = BeaconPredicate(id=identifier, edge_label=edge_label, frequency=count)

			predicates.append(p)

	return predicates
