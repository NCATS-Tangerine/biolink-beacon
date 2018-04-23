import requests

from swagger_server.models.beacon_concept import BeaconConcept  # noqa: E501
from swagger_server.models.beacon_concept_with_details import BeaconConceptWithDetails  # noqa: E501
from swagger_server.models.beacon_concept_detail import BeaconConceptDetail

from controller_impl import utils

def get_concept_details(conceptId):  # noqa: E501
    """get_concept_details

    Retrieves details for a specified concepts in the system, as specified by a (url-encoded) CURIE identifier of a concept known the given knowledge source.  # noqa: E501

    :param conceptId: (url-encoded) CURIE identifier of concept of interest
    :type conceptId: str

    :rtype: List[BeaconConceptWithDetails]
    """

    json_response = requests.get(
        utils.base_path() + 'bioentity/' + conceptId
    ).json()

    json_response = {k : v for k, v in json_response.items() if v is not None}

    concept = BeaconConceptWithDetails(
        id=json_response.get('id', None),
        name=json_response.get('label', None),
        type=' '.join(json_response.get('categories', [])),
        synonyms=json_response.get('synonyms', [])
    )

    return [concept]


def get_concepts(keywords, types=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_concepts

    Retrieves a (paged) list of whose concept in the beacon knowledge base with names and/or synonyms matching a set of keywords or substrings. The (possibly paged) results returned should generally be returned in order of the quality of the match, that is, the highest ranked concepts should exactly match the most keywords, in the same order as the keywords were given. Lower quality hits with fewer keyword matches or out-of-order keyword matches, should be returned lower in the list.  # noqa: E501

    :param keywords: a (urlencoded) space delimited set of keywords or substrings against which to match concept names and synonyms
    :type keywords: str
    :param types: a (url-encoded) space-delimited set of semantic groups (specified as codes CHEM, GENE, ANAT, etc.) to which to constrain concepts matched by the main keyword search (see [Semantic Groups](https://metamap.nlm.nih.gov/Docs/SemGroups_2013.txt) for the full list of codes)
    :type types: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of concepts per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[BeaconConcept]
    """

    json_response = requests.get(
        utils.base_path() + 'search/entity/' + ' '.join(keywords),
        params={
            'rows': pageSize,
            'start': pageNumber,
            'category': types
        }
    ).json()

    concepts = []

    for d in json_response['docs']:
        name = utils.sanitize_str(utils.get_property(d, 'label'))
        category = utils.sanitize_str(utils.get_property(d, 'category'))
        definition = utils.sanitize_str(utils.get_property(d, 'definition'))

        concept = BeaconConcept(
            id=utils.get_property(d, 'id'),
            name=name,
            type=category,
            synonyms=utils.get_property(d, 'synonym', []),
            definition=definition
        )

        concepts.append(concept)

    return concepts
