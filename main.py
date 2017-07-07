"""
Copyright (c) 2017 NCATS Data Translator Project - Tangerine Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask import abort

import requests

from ontobio.golr.golr_query import GolrSearchQuery
from ontobio.golr.golr_query import GolrAssociationQuery
from ontobio.config import session

# Set absolute path of configuration file
import os
abspath = os.path.abspath(os.path.dirname(__file__))
session.default_config_path = abspath + '/conf/config.yaml'

app = Flask(__name__)

@app.route('/')
def hello_world():
    response = {}
    response['wraps'] = 'https://api.monarchinitiative.org/api/'
    response['name'] = 'Monarch Biolink Knowledge Beacon'
    response['github'] = 'https://github.com/NCATS-Tangerine/biolink-beacon'
    return jsonify(response)

@app.route('/concepts/')
@app.route('/concepts')
def get_concepts():
    keywords = request.args.get('keywords', None)
    semgroups = request.args.get('semgroups', None)
    pageSize = int(request.args.get('pageSize', 1))
    pageNumber = int(request.args.get('pageNumber', 1))

    if keywords == None or pageSize < 1 or pageNumber < 1:
        abort(404)

    q = GolrSearchQuery(
        term=keywords,
        category=build_categories(semgroups),
        rows=pageSize,
        start=getStartIndex(pageNumber, pageSize)
    )

    results = q.exec()

    concepts = []
    for d in results['docs']:
        concept = parse_concept(d)
        concepts.append(concept)

    return jsonify(concepts)

@app.route('/concepts/<string:conceptId>/')
@app.route('/concepts/<string:conceptId>')
def get_concept_details(conceptId):
    r = requests.get('https://api.monarchinitiative.org/api/bioentity/' + conceptId + '?rows=1')
    concept = parse_concept(r.json())
    return jsonify([concept])

@app.route('/statements/')
@app.route('/statements')
def get_statements():
    keywords = request.args.get('keywords', None)
    semgroups = request.args.get('semgroups', None)
    pageSize = int(request.args.get('pageSize', 1))
    pageNumber = int(request.args.get('pageNumber', 1))
    c = request.args.getlist('c')

    if c == [] or pageSize < 1 or pageNumber < 1:
        abort(404)

    q = GolrAssociationQuery(
        subject_or_object_ids=c,
        subject_or_object_category=build_categories(semgroups),
        rows=pageSize,
        start=getStartIndex(pageNumber, pageSize)
    )

    results = q.exec()

    key_pairs = { 'id' : 'id', 'name' : 'label' }

    statements = []
    for d in results['associations']:
        try:
            statement = {}
            statement['id'] = d['id']
            statement['object'] = {k1 : d['object'].get(k2, None) for k1, k2 in key_pairs.items() }
            statement['subject'] = {k1 : d['subject'].get(k2, None) for k1, k2 in key_pairs.items() }
            statement['predicate'] = {k1 : d['relation'].get(k2, None) for k1, k2 in key_pairs.items() }
        except:
            pass

        statements.append(statement)

    return jsonify(statements)

@app.route('/evidence/<string:statementId>/')
@app.route('/evidence/<string:statementId>')
def get_evidence(statementId):
    evidence = {}
    evidence['date'] = '2017-05-10'
    evidence['id'] = 'https://monarchinitiative.org/'
    evidence['label'] = 'From the Monarch Initiative'

    evidences = [evidence]
    return jsonify(evidences)

@app.route('/exactmatches/<string:conceptId>/')
@app.route('/exactmatches/<string:conceptId>')
def get_exactmatches_by_conceptId(conceptId):
    return jsonify(find_exactmaches(conceptId))

@app.route('/exactmatches/')
@app.route('/exactmatches')
def get_exactmatches_by_concept_id_list():
    c = request.args.getlist('c')

    if c == []:
        abort(404)
    else:
        exactmatches = []
        for conceptId in c:
            exactmatches.append(find_exactmatches(conceptId))
        return jsonify(exactmatches)

def find_exactmaches(conceptId):
    """
    Returns a set of concept ID's that are exact maches for the given conceptId
    """
    q = GolrSearchQuery(
        term=conceptId,
        rows=5
    )
    results = q.exec()

    docs = results['docs']

    for d in docs:
        if get_concept_property(d, 'id') == conceptId:
            exactmatches = get_concept_property(d, 'equivalent_curie')
            return jsonify([]) if exactmatches == None else exactmatches
    return jsonify([])

def get_concept_property(d, key):
    """
    Exhausts each affix before returning nothing.

    Parameters
    ----------
    d : dict
        representing a monarch bioentity
    key : str
        the key of the property to be obtained
    """
    affixes = ['_eng', '_std', '_kw']
    try:
        return d[key]
    except:
        for affix in affixes:
            try:
                return d[key + affix]
            except:
                None
    return None

def parse_concept(d):
    """
    Returns a dict in the form of a tkbio concept

    Parameters
    ----------
    d : dict
        representing a monarch bioentity
    """
    key_pairs = {
        'id' : 'id',
        'synonyms' : 'synonym',
        'definition' : 'definition',
        'semanticGroup' : 'category',
        'name' : 'label'
    }

    concept = { k1 : get_concept_property(d, k2) for k1, k2 in key_pairs.items() }

    # These properties are sometimes encoded as lists, but we need them to be strings
    keys = 'definition', 'semanticGroup', 'name'
    for key in keys:
        if isinstance(concept[key], list):
            concept[key] = ', '.join(concept[key])

    # Sometimes bioentities have a 'categories' rather than 'category' field
    categories = d.get('categories', None)
    if concept['semanticGroup'] is None and categories is not None:
        concept['semanticGroup'] = ' '.join(monarch_to_UMLS(categories))
    else:
        concept['semanticGroup'] = monarch_to_UMLS(concept['semanticGroup'])

    return concept

def build_categories(semgroups):
    """
    Returns a list of ontobio categories or None

    Parameters
    ----------
    semgroups : string
        a space deliminated collection of semgroups
    """
    if semgroups is None:
        return None

    categories = []
    for semgroup in semgroups.split(' '):
        try:
            categories += UMLS_to_monarch(semgroup.upper())
        except:
            None

    if len(categories) == 0:
        return None
    else:
        return categories

# TODO: Make sure that this mapping makes sense!
# https://github.com/monarch-initiative/SciGraph-docker-monarch-data/blob/master/src/main/resources/monarchLoadConfiguration.yaml.tmpl#L74-L113

semantic_mapping = {
    'GENE' : ['gene', 'genotype', 'reagent targeted gene', 'intrinsic genotype', 'extrinsic genotype', 'effective genotype', 'haplotype', 'chromosome'],
    'ANAT' : ['anatomical entity', 'cellular component'],
    'LIVB' : ['cell', 'multi-cellular organism', 'organism'],
    'OBJC' : ['quality', 'cell line', 'molecular entity', 'variant locus', 'sequence alteration', 'sequence feature', 'evidence', 'pathway', 'publication', 'case', 'association'],
    'DISO' : ['disease'],
    'PROC' : ['assay'],
    'CONC' : ['age'],
    'CHEM' : ['drug', 'protein'],
    'PHYS' : ['Phenotype', 'molecular function'],
    'PHEN' : ['biological process'],
    # Nothing fits in these categories?
    'ACTI' : [''],
    'DEVI' : [''],
    'GEOG' : [''],
    'OCCU' : [''],
    'ORGA' : ['']
}

def UMLS_to_monarch(semgroup):
    if semgroup is None: return None

    if isinstance(semgroup, (list, set)):
        return list({ UMLS_to_monarch(c) for c in semgroup })
    else:
        # None translates to any semantic category, an empty string translates
        # to no semantic category.
        return semantic_mapping.get(semgroup.upper(), '')

def monarch_to_UMLS(category):
    if category is None: return 'OBJC'

    if isinstance(category, (list, set)):
        return list({ monarch_to_UMLS(c) for c in category })
    else:
        for key, value in semantic_mapping.items():
            if category in value:
                return key
        return 'OBJC'

def getStartIndex(pageNumber, pageSize):
    """
    Monarch begins its indexing at zero, and start refers to the index of
    the data rather than the page number. This method calculates the start index
    from the pageNumber and pageSize
    """
    return (pageNumber - 1) * pageSize
