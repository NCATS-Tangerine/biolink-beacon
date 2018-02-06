import connexion
import six

from swagger_server.models.concept import Concept  # noqa: E501
from swagger_server.models.concept_with_details import ConceptWithDetails  # noqa: E501
from swagger_server import util


def get_concept_details(conceptId):  # noqa: E501
    """get_concept_details

    Retrieves details for a specified concepts in the system, as specified by a (url-encoded) CURIE identifier of a concept known the given knowledge source.  # noqa: E501

    :param conceptId: (url-encoded) CURIE identifier of concept of interest
    :type conceptId: str

    :rtype: List[ConceptWithDetails]
    """
    return 'do some magic!'


def get_concepts(keywords, semanticGroups=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_concepts

    Retrieves a (paged) list of whose concept in the beacon knowledge base with names and/or synonyms matching a set of keywords or substrings. The (possibly paged) results returned should generally be returned in order of the quality of the match, that is, the highest ranked concepts should exactly match the most keywords, in the same order as the keywords were given. Lower quality hits with fewer keyword matches or out-of-order keyword matches, should be returned lower in the list.  # noqa: E501

    :param keywords: a (urlencoded) space delimited set of keywords or substrings against which to match concept names and synonyms
    :type keywords: str
    :param semanticGroups: a (url-encoded) space-delimited set of semantic groups (specified as codes CHEM, GENE, ANAT, etc.) to which to constrain concepts matched by the main keyword search (see [Semantic Groups](https://metamap.nlm.nih.gov/Docs/SemGroups_2013.txt) for the full list of codes)
    :type semanticGroups: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of concepts per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[Concept]
    """

    pageNumber = 1 if pageNumber == None or pageNumber < 1 else pageNumber
    pageSize = 5 if pageSize == None or pageSize < 1 else pageSize

    concept = Concept(
        id='biolink:123',
        name='Biolink concepts relating to: ' + keywords,
        semantic_group='GENE',
        synonyms=[],
        definition='no definition available'
    )

    return [concept for i in range(pageSize)]
