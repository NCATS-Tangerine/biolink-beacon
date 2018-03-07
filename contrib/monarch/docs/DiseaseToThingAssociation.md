---
layout: default
---

## disease to thing association


None

URI: [http://bioentity.io/vocab/DiseaseToThingAssociation](http://bioentity.io/vocab/DiseaseToThingAssociation)
## Mappings


## Inheritance

 *  is_a: [association](Association.html)

## Children

 *  mixin: [disease to phenotypic feature association](DiseaseToPhenotypicFeatureAssociation.html)
 *  mixin: [disease to phenotypic feature association](DiseaseToPhenotypicFeatureAssociation.html)


## Fields

 * [association type](association_type.html)
    * _connects an association to the type of association (e.g. gene to phenotype)_
    * __range__: [ontology class](OntologyClass.html)
    * inherited from: [association](Association.html)
 * [subject](subject.html)
    * _disease class_
    * __range__: [disease](Disease.html) [required]
    * Example: [MONDO:0017314](http://purl.obolibrary.org/obo/MONDO_0017314) Ehlers-Danlos syndrome, vascular type
    * inherited from: [association](Association.html)
 * [negated](negated.html)
    * _if set to true, then the association is negated i.e. is not true_
    * __range__: boolean
    * inherited from: [association](Association.html)
 * [relation](relation.html)
    * _the relationship type by which a subject is connected to an object in an association_
    * __range__: [relationship type](RelationshipType.html) [required]
    * inherited from: [association](Association.html)
 * [object](object.html)
    * _connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object._
    * __range__: None [required]
    * inherited from: [association](Association.html)
 * [qualifiers](qualifiers.html)
    * _connects an association to qualifiers that modify or qualify the meaning of that association_
    * __range__: [ontology class](OntologyClass.html)*
    * inherited from: [association](Association.html)
 * [publications](publications.html)
    * _connects an association to publications supporting the association_
    * __range__: [publication](Publication.html)*
    * inherited from: [association](Association.html)
 * [provided by](provided_by.html)
    * _connects an association to the agent (person, organization or group) that provided it_
    * __range__: [provider](Provider.html)
    * inherited from: [association](Association.html)
 * [id](id.html)
    * __range__: identifier type
    * inherited from: [named thing](NamedThing.html)
 * [label](label.html)
    * _A human-readable name for a thing_
    * __range__: label type
    * inherited from: [named thing](NamedThing.html)
 * [subject extensions](subject_extensions.html)
    * _Additional relationships that are true of the subject in the context of the association. For example, if the subject is a gene product in a functional association, the subject extensions may represent  an isoform or a specific post-translational state_
    * __range__: [property value pair](PropertyValuePair.html)*
    * inherited from: [extensions and evidence association mixin](ExtensionsAndEvidenceAssociationMixin.html)
 * [object extensions](object_extensions.html)
    * _Additional relationships that are true of the object in the context of the association. For example, if the object is an anatomical term in an expression association, the object extensions may include part-of links_
    * __range__: [property value pair](PropertyValuePair.html)*
    * inherited from: [extensions and evidence association mixin](ExtensionsAndEvidenceAssociationMixin.html)
 * [has evidence graph](has_evidence_graph.html)
    * _connects an association to a graph object including a path from subject to object_
    * __range__: evidence graph
    * inherited from: [extensions and evidence association mixin](ExtensionsAndEvidenceAssociationMixin.html)
 * [has evidence type](has_evidence_type.html)
    * _connects an association to the class of evidence used_
    * __range__: [evidence type](EvidenceType.html)
    * inherited from: [extensions and evidence association mixin](ExtensionsAndEvidenceAssociationMixin.html)
 * [has evidence](has_evidence.html)
    * _connects an association to an instance of supporting evidence_
    * __range__: evidence instance
    * inherited from: [extensions and evidence association mixin](ExtensionsAndEvidenceAssociationMixin.html)
 * [subject taxon](subject_taxon.html)
    * _the taxonomic class of the entity in the object slot_
    * __range__: [organism taxon](OrganismTaxon.html)
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [subject taxon label](subject_taxon_label.html)
    * __range__: label
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [subject taxon closure](subject_taxon_closure.html)
    * _The taxon class or ancestor class for the subject_
    * __range__: [ontology class](OntologyClass.html)*
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [subject taxon closure label](subject_taxon_closure_label.html)
    * _The label for the taxon class or ancestor class for the subject_
    * __range__: label type*
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [object taxon](object_taxon.html)
    * _the taxonomic class of the entity in the object slot_
    * __range__: [organism taxon](OrganismTaxon.html)
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [object taxon label](object_taxon_label.html)
    * __range__: label
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [object taxon closure](object_taxon_closure.html)
    * _The taxon class or ancestor class for the object_
    * __range__: [ontology class](OntologyClass.html)*
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)
 * [object taxon closure label](object_taxon_closure_label.html)
    * _The label for the taxon class or ancestor class for the object_
    * __range__: label type*
    * inherited from: [taxon closure mixin](TaxonClosureMixin.html)