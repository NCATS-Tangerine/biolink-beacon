import connexion
import six

from swagger_server.models.beacon_concept_type import BeaconConceptType  # noqa: E501
from swagger_server.models.beacon_knowledge_map_statement import BeaconKnowledgeMapStatement  # noqa: E501
from swagger_server.models.beacon_predicate import BeaconPredicate  # noqa: E501
from swagger_server import util

import controller_impl

def get_concept_types():  # noqa: E501
    """get_concept_types

    Get a list of types and # of instances in the knowledge source, and a link to the API call for the list of equivalent terminology  # noqa: E501


    :rtype: List[BeaconConceptType]
    """
    return controller_impl.get_concept_types()


def get_knowledge_map():  # noqa: E501
    """get_knowledge_map

    Get a high level knowledge map of the all the beacons by subject semantic type, predicate and semantic object type  # noqa: E501


    :rtype: List[BeaconKnowledgeMapStatement]
    """
    return controller_impl.get_knowledge_map()


def get_predicates():  # noqa: E501
    """get_predicates

    Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


    :rtype: List[BeaconPredicate]
    """
    return controller_impl.get_predicates()
