import requests

from swagger_server.models.beacon_concept import BeaconConcept  # noqa: E501
from swagger_server.models.beacon_concept_with_details import BeaconConceptWithDetails  # noqa: E501
from swagger_server.models.beacon_concept_detail import BeaconConceptDetail

from controller_impl import utils

def get_concept_details(conceptId):
    response = requests.get(utils.base_path() + 'bioentity/' + conceptId)

    if response.status_code != 200:
        raise Exception(response.url + " returned status code: " + str(response.status_code))

    json_response = response.json()

    json_response = {k : v for k, v in json_response.items() if v is not None}

    synonyms = [d.get('val') for d in json_response.get('synonyms', []) if d.get('val') != None]

    categories = [utils.map_category(c) for c in json_response.get('categories', [])]

    concept = BeaconConceptWithDetails(
        id=json_response.get('id', None),
        uri=json_response.get('iri', None),
        name=json_response.get('label', None),
        symbol=None,
        categories=categories,
        description=json_response.get('description', None),
        synonyms=synonyms
    )

    return [concept] if concept.id == conceptId else []

def get_concepts(keywords, categories=None, size=None):
    size = utils.sanitize_int(size, 10)

    params = {}

    if categories is not None:
        categories = [utils.map_category(t) for t in categories]
        params['category'] = categories

    if size is not None:
        params['rows'] = size

    json_response = requests.get(
        utils.base_path() + 'search/entity/' + ' '.join(keywords),
        params=params
    )

    json_response = json_response.json()

    concepts = []

    for d in json_response['docs']:
        _categories = utils.get_property(d, 'category')

        if isinstance(_categories, list):
            _categories = [utils.map_category(c) for c in _categories]
        elif isinstance(_categories, str):
            _categories = [utils.map_category(_categories)]

        name = utils.sanitize_str(utils.get_property(d, 'label'))

        synonym = utils.get_property(d, 'synonym', [])

        definition = utils.sanitize_str(utils.get_property(d, 'definition'))
        definition = None if definition == 'None' else definition

        concept = BeaconConcept(
            id=utils.get_property(d, 'id'),
            name=name,
            categories=_categories,
            description=definition
        )

        concepts.append(concept)

    return concepts
