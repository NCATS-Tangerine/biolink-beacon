from ontobio.golr.golr_query import GolrAssociationQuery, M
from swagger_server.models.beacon_predicate import BeaconPredicate

from controller_impl import utils

_PREDICATES='predicates.json'

def get_predicates():
	"""get_predicates

	Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


	:rtype: List[Predicate]
	"""

	cached_predicates = utils.load(_PREDICATES)
	if cached_predicates != None:
		return [dictToPredicate(d) for d in cached_predicates]

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
			name = pivot['value']
			# not currently used
			count = pivot['count']

			predicates.append({
				'id' : identifier,
				'name' : name,
				'count' : count
			})

	utils.save(predicates, _PREDICATES)

	return [dictToPredicate(d) for d in predicates]

def dictToPredicate(d):
	return BeaconPredicate(id=d['id'], name=d['name'], definition=None)
