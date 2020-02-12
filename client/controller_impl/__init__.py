"""
Implementation methods are imported here so that they can be used in the
following way:

import controller_impl; controller_impl.get_concept_details(conceptId);

This makes their use in the server sub-project more simple.
"""

from controller_impl.concepts_controller_impl import get_concept_details, get_concepts
from controller_impl.evidence_controller_impl import get_statement_details
from controller_impl.exactmatches_controller_impl import get_exact_matches_to_concept_list
from controller_impl.metadata_controller_impl import get_knowledge_map, get_concept_categories
from controller_impl.predicates_controller_impl import get_predicates
from controller_impl.statements_controller_impl import get_statements
