import requests

from swagger_server.models.annotation import Annotation  # noqa: E501

from controller_impl import utils


def get_evidence(statementId, keywords=None, pageNumber=None, pageSize=None):  # noqa: E501
    """get_evidence

    Retrieves a (paged) list of annotations cited as evidence for a specified concept-relationship statement  # noqa: E501

    :param statementId: (url-encoded) CURIE identifier of the concept-relationship statement (\&quot;assertion\&quot;, \&quot;claim\&quot;) for which associated evidence is sought
    :type statementId: str
    :param keywords: (url-encoded, space delimited) keyword filter to apply against the label field of the annotation
    :type keywords: str
    :param pageNumber: (1-based) number of the page to be returned in a paged set of query results
    :type pageNumber: int
    :param pageSize: number of cited references per page to be returned in a paged set of query results
    :type pageSize: int

    :rtype: List[Annotation]
    """
    pageNumber = utils.sanitize_int(pageNumber)
    pageSize = utils.sanitize_int(pageSize, default_value=5)

    prefix = utils.biolink_prefix() + ':'
    if statementId.startswith(prefix):
        statementId = statementId[len(prefix):]

    path = utils.base_path() + 'association/' + statementId
    params = {'page' : pageNumber - 1, 'rows' : pageSize}

    json_response = requests.get(path, params).json()

    publications = json_response['publications']

    annotations = []

    if publications != None and publications != []:
        for publication in publications:
            annotation = Annotation(
                id=publication.get('id', ''),
                label=publication.get('label', 'unspecified PubMed article')
            )
            annotations.append(annotation)

    return annotations
