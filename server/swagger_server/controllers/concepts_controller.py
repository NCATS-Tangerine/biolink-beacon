import connexion
import six

from swagger_server.models.beacon_concept import BeaconConcept  # noqa: E501
from swagger_server.models.beacon_concept_with_details import BeaconConceptWithDetails  # noqa: E501
from swagger_server import util

import controller_impl

def get_concept_details(conceptId):  # noqa: E501
    """get_concept_details

    Retrieves details for a specified concepts in the system, as specified by a (url-encoded) CURIE identifier of a concept known the given knowledge source.  # noqa: E501

    :param conceptId: (url-encoded) CURIE identifier of concept of interest
    :type conceptId: str

    :rtype: List[BeaconConceptWithDetails]
    """
    return controller_impl.get_concept_details(conceptId)


def get_concepts(keywords, types=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_concepts

    Retrieves a (paged) list of whose concept in the beacon knowledge base with names and/or synonyms matching a set of keywords or substrings. The (possibly paged) results returned should generally be returned in order of the quality of the match, that is, the highest ranked concepts should exactly match the most keywords, in the same order as the keywords were given. Lower quality hits with fewer keyword matches or out-of-order keyword matches, should be returned lower in the list.  # noqa: E501

    :param keywords: a (urlencoded) space delimited set of keywords or substrings against which to match concept names and synonyms
    :type keywords: str
    :param types: a (url-encoded) space-delimited set of semantic groups (specified as codes gene, pathway, etc.) to which to constrain concepts matched by the main keyword search (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)
    :type types: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of concepts per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[BeaconConcept]
    """
    return controller_impl.get_concepts(keywords, types, pageNumber, pageSize)


def get_exact_matches_to_concept(conceptId):  # noqa: E501
    """get_exact_matches_to_concept

    Retrieves a list of qualified identifiers of \&quot;exact match\&quot; concepts, [sensa SKOS](http://www.w3.org/2004/02/skos/core#exactMatch) associated with a specified (url-encoded) CURIE (without brackets) concept object identifier,  typically, of a concept selected from the list of concepts originally returned by a /concepts API call on a given KS.  # noqa: E501

    :param conceptId: (url-encoded) CURIE identifier of the concept to be matched
    :type conceptId: str

    :rtype: List[str]
    """
    return controller_impl.get_exact_matches_to_concept(conceptId)


def get_exact_matches_to_concept_list(c):  # noqa: E501
    """get_exact_matches_to_concept_list

    Given an input list of [CURIE](https://www.w3.org/TR/curie/) identifiers of known exactly matched concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch), retrieves the list of [CURIE](https://www.w3.org/TR/curie/) identifiers of additional concepts that are deemed by the given knowledge source to be exact matches to one or more of the input concepts **plus** whichever identifiers from the input list which specifically matched these new additional concepts.  If an empty set is returned, the it can be assumed that the given  knowledge source does not know of any new equivalent concepts matching the input set.  # noqa: E501

    :param c: set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of exactly matching concepts, to be used in a search for additional exactly matching concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch).
    :type c: List[str]

    :rtype: List[str]
    """
    return controller_impl.get_exact_matches_to_concept_list(c)
