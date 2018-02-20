from swagger_server.models.summary import Summary
from ontobio.golr.golr_query import GolrAssociationQuery, M

def linked_types():
    """linked_types

    Get a list of types and # of instances in the knowledge source, and a link to the API call for the list of equivalent terminology  # noqa: E501


    :rtype: List[Summary]
    """
    g = GolrAssociationQuery(
        q='*:*',
        facet_fields=[M.OBJECT_CATEGORY, M.SUBJECT_CATEGORY],
        rows=0
    )

    results = g.exec()

    object_category = results['facet_counts']['object_category']
    subject_category = results['facet_counts']['subject_category']

    counts = __build_category_counts(object_category)
    counts = __build_category_counts(subject_category, counts=counts)

    summaries = []

    for category in counts:
        summary = Summary(id=category, frequency=counts[category], idmap=None)
        summaries.append(summary)

    return summaries

def __build_category_counts(d, counts={}):
    for k in d.keys():
        if k not in counts:
            counts[k] = d[k]
        else:
            count = counts.get(k)
            counts[k] = count + d[k]
    return counts
