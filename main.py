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

from ontobio.ontobio.golr.golr_query import GolrSearchQuery
from ontobio.ontobio.golr.golr_query import GolrAssociationQuery

app = Flask(__name__)

@app.route('/')
def hello_world():
    response = {}
    response['author'] = 'Lance Hannestad'
    response['wraps'] = 'https://api.monarchinitiative.org/api/'
    response['name'] = 'biolink'
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

    q = GolrSearchQuery(term=keywords, category=semgroups, rows=pageSize, start=pageNumber)
    results = q.exec()

    concepts = []
    print('len:', len(results['docs']))
    for d in results['docs']:
        concept = parse_consept(d)
        concepts.append(concept)

    return jsonify(concepts)

@app.route('/concepts/<string:conceptId>/')
@app.route('/concepts/<string:conceptId>')
def get_concept_details(conceptId):
    q = GolrSearchQuery(term=conceptId, rows=5)
    results = q.exec()
    concepts = []
    for d in results['docs']:
        if get_concept_property(d, 'id') == conceptId:
            concepts.append(parse_consept(d))
    return jsonify(concepts)

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

    q = GolrAssociationQuery(subject_or_object_ids=c, rows=pageSize, start=pageNumber)
    results = q.exec()

    key_pairs = { 'id' : 'id', 'name' : 'label' }

    statements = []
    print('len:', len(results['associations']))
    for d in results['associations']:
        try:
            statement = {}
            statement['id'] = d['id']
            statement['object'] = { k1 : d['object'][k2] for k1, k2 in key_pairs.items() }
            statement['subject'] = { k1 : d['subject'][k2] for k1, k2 in key_pairs.items() }
            statement['predicate'] = {k1 : d['relation'][k2] for k1, k2 in key_pairs.items() }
            statements.append(statement)
        except:
            None

    return jsonify(statements)

@app.route('/evidence/<string:statementId>/')
@app.route('/evidence/<string:statementId>')
def get_evidence(statementId):
    evidence = {}
    evidence['date'] = '3000-01-01'
    evidence['id'] = 'https://monarchinitiative.org/'
    evidence['label'] = 'From the Monarch Initiative'

    evidences = [evidence]
    return jsonify(evidences)

@app.route('/exactmatches/<string:conceptId>/')
@app.route('/exactmatches/<string:conceptId>')
def get_exactmatches_by_conceptId(conceptId):
    q = GolrSearchQuery(term=conceptId, rows=5)
    results = q.exec()
    # return jsonify(results)

    d = results['docs']

    for concept in d:
        if concept['id'] == conceptId:
            exactmatches = get_concept_property(concept, 'equivalent_curie')
            exactmatches = [] if exactmatches == None else exactmatches
            return jsonify(exactmatches)
    return jsonify([])

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

def find_exactmaches(conceptId):
    """
    Returns a set of concept ID's that are exact maches for the given conceptId
    """
    q = GolrSearchQuery(term=conceptId, rows=5)
    results = q.exec()

    docs = results['docs']

    for d in docs:
        if get_concept_property(d, 'id') == conceptId:
            exactmatches = get_concept_property(d, 'equivalent_curie')
            return [] if exactmatches == None else exactmatches
    return []

def parse_consept(d):
    """
    Returns a dict in the form of a tkbio concept

    Parameters
    ----------
    d : dict
        representing a monarch bioentity
    """
    key_pairs = {                       \
        'id' : 'id',                    \
        'synonyms' : 'synonym',         \
        'definition' : 'definition',    \
        'semanticGroup' : 'category',   \
        'name' : 'label'                \
    }

    concept = { k1 : get_concept_property(d, k2) for k1, k2 in key_pairs.items() }

    # These properties are encoded as lists in monarch, but we need them to be strings
    keys = 'synonyms', 'definition', 'semanticGroup', 'name'
    for key in keys:
        if concept[key] is not None:
            concept[key] = ', '.join(concept[key])

    return concept
