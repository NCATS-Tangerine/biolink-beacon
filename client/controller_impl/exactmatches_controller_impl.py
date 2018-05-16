from controller_impl import utils
from ontobio.golr.golr_query import GolrSearchQuery

from swagger_server.models.exact_match_response import ExactMatchResponse

from cachetools.func import ttl_cache

def get_exact_matches_to_concept_list(c):  # noqa: E501
    """get_exact_matches_to_concept_list

    Given an input list of [CURIE](https://www.w3.org/TR/curie/) identifiers of known exactly matched concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch), retrieves the list of [CURIE](https://www.w3.org/TR/curie/) identifiers of additional concepts that are deemed by the given knowledge source to be exact matches to one or more of the input concepts **plus** whichever identifiers from the input list which specifically matched these new additional concepts.  If an empty set is returned, the it can be assumed that the given  knowledge source does not know of any new equivalent concepts matching the input set.  # noqa: E501

    :param c: set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of exactly matching concepts, to be used in a search for additional exactly matching concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch).
    :type c: List[str]

    :rtype: List[str]
    """

    s = []
    for conceptId in c:
        e = _get_exact_matches(conceptId)
        s.append(e)

    return s

# ttl is "time to live" in seconds
@ttl_cache(maxsize=1000, ttl=86400)
def _get_exact_matches(conceptId):
    results = GolrSearchQuery(
        term=conceptId,
        fq={'id' : conceptId},
        rows=1,
        hl=False
    ).search()

    docs = results.docs

    exactmatches = []

    for d in docs:
        if  utils.get_property(d, 'id') == conceptId:
            matches = utils.get_property(d, 'equivalent_curie', [])
            exactmatches.extend(matches)

    e = ExactMatchResponse(
        id=conceptId,
        within_domain=len(docs) != 0,
        has_exact_matches=exactmatches
    )

    return e
