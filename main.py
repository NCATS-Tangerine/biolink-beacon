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
    semanticGroups = request.args.get('semanticGroups', None)
    pageSize = int(request.args.get('pageSize', 1))
    pageNumber = int(request.args.get('pageNumber', 1))

    validatePagination(pageSize, pageNumber)
    validateKeywords(keywords)

    q = GolrSearchQuery(
        term=keywords,
        category=build_categories(semanticGroups),
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
    
    if(conceptId.startswith("biolink"))
        conceptId = objectId(conceptId)
    
    results = GolrSearchQuery(
        term=conceptId,
        fq={'id' : conceptId},
        rows=1,
        hl=False
    ).exec()

    entries = []
    for d in results['docs']:
        
        c = parse_concept(d)

        details = {}
        details['iri'] = get_concept_property(d, 'iri')
        details['taxon'] = get_concept_property(d, 'taxon')
        details['taxon_label'] = get_concept_property(d, 'taxon_label')
        details['taxon_label_synonym'] = get_concept_property(d, 'taxon_label_synonym')

        if details['taxon_label_synonym'] is not None:
            details['taxon_label_synonym'] = ', '.join(details['taxon_label_synonym'])

        c['details'] = [{'tag' : k, 'value' : v} for k, v in details.items() if v is not None]

        entries += [c]

    return jsonify(entries)

def get_concept(conceptId):
    
    if conceptId.startswith("biolink"):
        conceptId = objectId(conceptId)
    
    results = GolrSearchQuery(
        term=conceptId,
        fq={'id' : conceptId},
        rows=1,
        hl=False
    ).exec() 
    
    c = None    
    entries = []
    for d in results['docs']:
        
        c = parse_concept(d)
        break
    
    return c

@app.route('/statements/')
@app.route('/statements')
def get_statements():
    keywords = request.args.get('keywords', None)
    semanticGroups = request.args.get('semanticGroups', None)
    relations = request.args.get('relations', None)
    pageSize = int(request.args.get('pageSize', 1))
    pageNumber = int(request.args.get('pageNumber', 1))
    c = getlist('c')

    validatePagination(pageNumber, pageSize)
    validateIdList(c)

    q = GolrAssociationQuery(
        subject_or_object_ids=c,
        subject_or_object_category=build_categories(semanticGroups),
        #relation=get_relation(relations), # Currently only first relation in the list, if any, is taken?
        rows=pageSize,
        start=getStartIndex(pageNumber, pageSize),
        non_null_fields=['relation']
    )

    results = q.exec()
    
    #print("statement results: "+str(len(results['associations']))+" items found?")

    key_pairs = { 'id' : 'id', 'name' : 'label' }

    statements = []
    for d in results['associations']:
        try:
            statement = {}

            statement['id'] = 'biolink:' + d['id'] # add the biolink: prefix to statement id's
            
            statement['object'] = {k1 : d['object'][k2] for k1, k2 in key_pairs.items() }
            statement['object'] = get_concept(statement['object']['id'])
            
            statement['subject'] = {k1 : d['subject'][k2] for k1, k2 in key_pairs.items() }
            statement['subject'] = get_concept(statement['subject']['id'])
            
            statement['predicate'] = {k1 : d['relation'][k2] for k1, k2 in key_pairs.items() }

            statements.append(statement)

        except:
            pass

    return jsonify(statements)

@app.route('/evidence/<string:statementId>/')
@app.route('/evidence/<string:statementId>')
def get_evidence(statementId):
    
    if statementId.startswith('biolink:'):
        statementId = statementId[8:]
        
    evidences = []

    results = GolrAssociationQuery(id=statementId).exec()
    associations = results['associations']

    for association in associations:
        publications = association.get('publications', None)
        if publications != None:
            for publication in publications:
                evidence = {}
                evidence['id'] = publication.get('id', '')
                evidence['label'] = publication.get('label', 'PubMed article')
                evidence['date'] = '0000-0-00'

                evidences.append(evidence)

    # If the statement is found but has no associated publication, give a
    # generic response for evidence.
    if len(evidences) == 0 and len(associations) != 0:
        evidence = {}
        evidence['id'] = ''
        evidence['date'] = '0000-00-00'
        evidence['label'] = 'From the Monarch Initiative - No further supporting text'

        evidences.append(evidence)

    print(evidences)

    return jsonify(evidences)

@app.route('/exactmatches/<string:conceptId>/')
@app.route('/exactmatches/<string:conceptId>')
def get_exactmatches_by_conceptId(conceptId):
    return jsonify(find_exactmatches(conceptId))

@app.route('/exactmatches/')
@app.route('/exactmatches')
def get_exactmatches_by_concept_id_list():
    c = getlist('c')
    validateIdList(c)

    exactmatches = []
    for conceptId in c:
        exactmatches += find_exactmatches(conceptId)
    return jsonify(exactmatches)

@app.route('/types/')
@app.route('/types')
def get_types():
    
    frequency = {semanticGroup : 0 for semanticGroup in semantic_mapping.keys()}

    results = GolrAssociationQuery(
        rows=0,
        facet_fields=['subject_category', 'object_category']
    ).exec()

    facet_counts = results['facet_counts']

    subject_category = facet_counts['subject_category']
    object_category  = facet_counts['object_category']

    for key in subject_category:
        frequency[monarch_to_UMLS(key)] += subject_category[key]

    for key in object_category:
        frequency[monarch_to_UMLS(key)] += object_category[key]

    return jsonify([{'id' : c, 'idmap' : None, 'frequency' : f} for c, f in frequency.items()])

@app.route('/predicates/')
@app.route('/predicates')
def get_predicates():
    
    """
    I'm not quite sure how to best get at all the predicates and tag them as relations with id's
    """
    frequency = {semanticGroup : 0 for semanticGroup in semantic_mapping.keys()}

    results = GolrAssociationQuery(
        rows=0,
        facet_fields=['relation']
    ).exec()

    facet_counts = results['facet_counts']

    relations = facet_counts['relation']

    return jsonify([{'id' : "biolink:"+c, 'name' : c, 'definition' : None} for key in relations])

def find_exactmatches(conceptId):
    """
    Returns a list of concept ID's that are exact matches for the given conceptId
    """
    results = GolrSearchQuery(
        term=conceptId,
        fq={'id' : conceptId},
        rows=1,
        hl=False
    ).exec()

    docs = results['docs']

    for d in docs:
        if get_concept_property(d, 'id') == conceptId:
            exactmatches = get_concept_property(d, 'equivalent_curie')
            if exactmatches == None:
                exactmatches = [] # just in case this property is empty
            exactmatches.append(conceptId)
            return exactmatches if exactmatches != None else []
    return []

def get_concept_property(d, key):
    """
    Exhausts each affix before returning an empty string.

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
                pass
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

    if concept['definition'] is None:
        concept['definition'] = ""

    if concept['synonyms'] == None:
        concept['synonyms'] = []

    return concept

def build_categories(semanticGroups):
    """
    Returns a list of ontobio categories or None

    Parameters
    ----------
    semanticGroups : string
        a space delimited collection of semanticGroups
    """
    if semanticGroups is None:
        return None

    categories = []
    for semanticGroup in semanticGroups.split(' '):
        try:
            categories += UMLS_to_monarch(semanticGroup.upper())
        except:
            None

    if len(categories) == 0:
        return None
    else:
        return categories

def get_relation(relations):
    """
    Returns first entry in the list of relations or None

    Parameters
    ----------
    relations : string
        a space delimited collection of relation id's... but I only teke the first one? 
    """
    if relations is None:
        return None

    relation = None
    for relationId in relations.split(' '):
        try:
            relation = objectId(relationId)
            break # only first relation taken for now?
        except:
            None

    if relation == None:
        return None
    else:
        return relation

def objectId(id):
    idPart = id.split(":")
    id = idPart[1]
    return id

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

def UMLS_to_monarch(semanticGroup):
    if semanticGroup is None: return None

    if isinstance(semanticGroup, (list, set)):
        return list({ UMLS_to_monarch(c) for c in semanticGroup })
    else:
        # None translates to any semantic category, an empty string translates
        # to no semantic category.
        return semantic_mapping.get(semanticGroup.upper(), '')

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

def getlist(param_name):
    """
    Flask only handles lists like /statements?c=ABC&c=DEF&c=GHI
    But at the moment TKBio is formatting lists like /statements?c=ABC,DEF,GHI
    """
    l = request.args.getlist(param_name)
    c = []
    for item in l:
        c += item.split(',')
    return [item.strip() for item in c]

def validatePagination(pageSize, pageNumber):
    if pageSize < 1:
        abort(500, 'pageSize must be greater than zero')
    if pageNumber < 1:
        abort(500, 'pageNumber must be greater than zero')

def validateKeywords(keywords):
    if keywords is None:
        abort(500, 'keywords must not be empty')

def validateIdList(c):
    if c is []:
        abort(500, 'list c must not be empty')
