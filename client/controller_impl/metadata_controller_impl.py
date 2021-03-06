import requests

from ontobio.golr.golr_query import GolrSearchQuery, GolrAssociationQuery, M
from swagger_server.models.beacon_knowledge_map_statement import BeaconKnowledgeMapStatement
from swagger_server.models.beacon_knowledge_map_object import BeaconKnowledgeMapObject
from swagger_server.models.beacon_knowledge_map_subject import BeaconKnowledgeMapSubject
from swagger_server.models.beacon_knowledge_map_predicate import BeaconKnowledgeMapPredicate

from swagger_server.models.beacon_concept_category import BeaconConceptCategory

from cachetools.func import ttl_cache
from controller_impl import utils
from controller_impl.biolink import BiolinkTerm

_MONARCH_PREFIX_URI='https://api.monarchinitiative.org/api/identifier/prefixes/'

__time_to_live_in_seconds = 604800

@ttl_cache(maxsize=300, ttl=__time_to_live_in_seconds)
def get_concept_categories():  # noqa: E501
	"""get_concept_types

	Get a list of types and # of instances in the knowledge source, and a link to the API call for the list of equivalent terminology  # noqa: E501


	:rtype: List[BeaconConceptType]
	"""

	g = GolrAssociationQuery(
		q='*:*',
		facet_fields=[M.OBJECT_CATEGORY, M.SUBJECT_CATEGORY],
		rows=0
	)

	results = utils.try_multi(method=g.exec)

	object_category = results['facet_counts']['object_category']
	subject_category = results['facet_counts']['subject_category']

	counts = __build_category_counts(object_category)
	counts = __build_category_counts(subject_category, counts=counts)

	types = []

	for category in counts:
		term = BiolinkTerm(utils.map_category(category))
		_id = term.curie()
		label = utils.map_category(category)
		frequency = counts[category]
		iri = term.uri()

		t = BeaconConceptCategory(id=_id, category=label, frequency=frequency, uri=iri)

		types.append(t)

	return types

@ttl_cache(maxsize=300, ttl=__time_to_live_in_seconds)
def get_knowledge_map():
	"""get_knowledge_map

	Get a high level knowledge map of the all the beacons by subject semantic type, predicate and semantic object type  # noqa: E501


	:rtype: List[KnowledgeMapStatement]
	"""

	pivots = [M.RELATION, M.RELATION_LABEL, M.OBJECT_CATEGORY, M.SUBJECT_CATEGORY]

	g = GolrAssociationQuery(
		q='*:*',
		facet_fields=[M.RELATION, M.RELATION_LABEL, M.OBJECT_CATEGORY, M.SUBJECT_CATEGORY],
		facet_pivot_fields=pivots,
		rows=0
	)

	results = utils.try_multi(method=g.exec)
	facet_pivot = results['facet_pivot']

	pivot_str = ','.join(pivots)

	statements = []

	category_prefix_map = __get_category_prefix_map()

	for p1 in facet_pivot[pivot_str]:
		relation_id = p1['value']
		for p2 in p1['pivot']:
			relation_label = p2['value']
			for p3 in p2['pivot']:
				object_category = utils.map_category(p3['value'])
				for p4 in p3['pivot']:
					subject_category = utils.map_category(p4['value'])
					count = p4['count']

					object_prefixes=[]
					subject_prefixes=[]

					for prefix in category_prefix_map.keys():
						for category in category_prefix_map[prefix].keys():
							if subject_category == category:
								subject_prefixes.append(prefix)
							if object_category == category:
								object_prefixes.append(prefix)

					map_object = BeaconKnowledgeMapObject(
						category=object_category,
						prefixes=object_prefixes
					)

					map_subject = BeaconKnowledgeMapSubject(
						category=subject_category,
						prefixes=subject_prefixes
					)

					map_predicate = BeaconKnowledgeMapPredicate(
						relation=relation_label
					)

					map_statement = BeaconKnowledgeMapStatement(
						subject=map_subject,
						object=map_object,
						predicate=map_predicate,
						frequency=count,
						description=map_subject.category+" "+map_predicate.relation.replace("_"," ")+" "+map_object.category
					)

					statements.append(map_statement)

	return statements

def __build_category_counts(d, counts=None):
	if counts is None:
		counts = {}

	for k in d.keys():
		if k not in counts:
			counts[k] = d[k]
		else:
			count = counts.get(k)
			counts[k] = count + d[k]
	return counts

# https://github.com/NCATS-Tangerine/translator-knowledge-beacon/blob/develop/api/types.csv
__idmaps = {
	'individual_organism' : ['SIO:010000'],
	'disease' : ['MONDO:0000001'],
	'phenotypic_feature' : ['UPHENO:0000001'],
	'chemical_substance' : ['SIO:010004'],
	'genomic_entity' : ['SO:0000110'],
	'genome' : ['SO:0001026'],
	'transcript' : ['SO:0000673'],
	'exon' : ['SO:0000147'],
	'coding_sequence' : ['SO:0000316'],
	'gene' : ['SO:0000704', 'SIO:010035'],
	'protein' : ['PR:000000001', 'SIO:010043'],
	'RNA_product' : ['CHEBI:33697'],
	'microRNA' : ['SO:0000276'],
	'macromolecular_complex' : ['GO:0032991', 'SIO:010046'],
	'gene_family' : ['NCIT:C20130'],
	'sequence_variant' : ['GENO:0000512'],
	'drug_exposure' : ['ECTO:0000509'],
	'treatment' : ['OGMS:0000090'],
	'biological_process' : ['GO:0008150'],
	'cellular_component' : ['GO:0005575'],
	'cell' : ['GO:0005623', 'SIO:010001']
}

def __lookup_idmaps(category):
	if category in __idmaps:
		return ', '.join(__idmaps[category])
	else:
		return ''

def __get_category_prefix_map():
	prefixes = requests.get(_MONARCH_PREFIX_URI).json()

	d = {}

	for prefix in prefixes:
		if prefix is "":
			continue

		g = GolrSearchQuery(
			term='id:' + prefix + '*',
			facet_fields=['category'],
			rows=0
		)

		results = g.search()
		facet_counts = results.facet_counts
		categories_count = facet_counts['category']

		for category in categories_count.keys():
			d[prefix] = {category : categories_count[category]}

	return d
