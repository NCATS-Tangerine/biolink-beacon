import requests

# from swagger_server.models.beacon_annotation import BeaconAnnotation
from swagger_server.models.beacon_statement_with_details import BeaconStatementWithDetails

from controller_impl import utils

__DEFAULT_PUBMED_LABEL = 'unspecified PubMed article'


def get_statement_details(statementId, keywords=None, size=10):
    prefix = utils.biolink_prefix() + ':'
    if statementId.startswith(prefix):
        statementId = statementId[len(prefix):]

    import pudb; pu.db

    path = utils.base_path() + 'association/' + statementId
    params = {'page' : 0, 'rows' : size}

    json_response = requests.get(path, params).json()

    s = BeaconStatementWithDetails(
        id=None,
        is_defined_by=None,
        provided_by=None,
        qualifiers=[],
        annotation=[],
        evidence=[]
    )

def parse_response(json_response:dict):
    publications = json_response.get('publications')

    annotations = []

    if publications != None and publications != []:
        for publication in publications:
            identifier=publication.get('id', '')

            is_pubmed = identifier.upper().startswith('PMID:')

            label = publication.get('label', None)
            label = __DEFAULT_PUBMED_LABEL if label is None and is_pubmed else label

            annotation = BeaconAnnotation(id=identifier, label=label)
            annotations.append(annotation)

    return annotations
