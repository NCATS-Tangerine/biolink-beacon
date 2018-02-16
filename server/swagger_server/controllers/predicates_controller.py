import connexion
import six

from swagger_server.models.predicate import Predicate  # noqa: E501
from swagger_server import util

import controller_impl.predicates_controller_impl as impl

def get_predicates():  # noqa: E501
    """get_predicates

    Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


    :rtype: List[Predicate]
    """
    return impl.get_predicates()
