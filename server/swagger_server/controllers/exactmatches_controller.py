import connexion
import six

from swagger_server import util

import controller_impl.exactmatches_controller_impl as impl

def get_exact_matches_to_concept(conceptId):  # noqa: E501
    """get_exact_matches_to_concept

    Retrieves a list of qualified identifiers of \&quot;exact match\&quot; concepts, [sensa SKOS](http://www.w3.org/2004/02/skos/core#exactMatch) associated with a specified (url-encoded) CURIE (without brackets) concept object identifier,  typically, of a concept selected from the list of concepts originally returned by a /concepts API call on a given KS.  # noqa: E501

    :param conceptId: (url-encoded) CURIE identifier of the concept to be matched
    :type conceptId: str

    :rtype: List[str]
    """
    return impl.get_exact_matches_to_concept(conceptId)


def get_exact_matches_to_concept_list(c):  # noqa: E501
    """get_exact_matches_to_concept_list

    Given an input list of [CURIE](https://www.w3.org/TR/curie/) identifiers of known exactly matched concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch), retrieves the list of [CURIE](https://www.w3.org/TR/curie/) identifiers of additional concepts that are deemed by the given knowledge source to be exact matches to one or more of the input concepts **plus** whichever identifiers from the input list which specifically matched these new additional concepts.  If an empty set is returned, the it can be assumed that the given  knowledge source does not know of any new equivalent concepts matching the input set.  # noqa: E501

    :param c: set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of exactly matching concepts, to be used in a search for additional exactly matching concepts [*sensa*-SKOS](http://www.w3.org/2004/02/skos/core#exactMatch).
    :type c: List[str]

    :rtype: List[str]
    """
    return impl.get_exact_matches_to_concept_list(c)
