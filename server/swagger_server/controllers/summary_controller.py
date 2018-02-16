import connexion
import six

from swagger_server.models.summary import Summary  # noqa: E501
from swagger_server import util

import controller_impl.summary_controller_impl as impl

def linked_types():  # noqa: E501
    """linked_types

    Get a list of types and # of instances in the knowledge source, and a link to the API call for the list of equivalent terminology  # noqa: E501


    :rtype: List[Summary]
    """
    return impl.linked_types()
