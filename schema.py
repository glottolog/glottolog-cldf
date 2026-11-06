from collections import namedtuple

from csvw.metadata import Column

ParamInfo = namedtuple('ParamInfo', 'dt name description url type')

#
# FIXME: can we get any of the stuff below from glottolog/glottolog/config?
#

PARAMETER_INFO = {
    'level': ParamInfo(
        Column.fromvalue(
            dict(datatype=dict(base='string', format='family|language|dialect'))),
        'Level',
        "The Glottolog classification imposes the following rules on the nesting of languoids:"
        " 1. Dialects must not be top-level nodes of the classification."
        " 2. Dialects must not have a family as parent."
        " 3. Languages must either be isolates (i.e. top-level nodes) or have a family as parent."
        " 4. The levels of the languoids in a tree branch must be monotonically descending."
        "\n"
        "Languoid level information needs to be interpreted in the context of the languoid's "
        "category. For languoids in 'non-genealogical trees' as described in "
        "[About languoids](about/languoids.md) the principles for determining "
        "language level languoids do not hold. "
        "Instead, in these cases, 'family' just means 'group of languoids', 'language' means "
        "'languoid with extended metadata such as coordinates', and 'dialect' mean any type of "
        "'sub-lect'.",
        'about/glossary.md#languoid',
        'categorical',
    ),
    'category': ParamInfo(
        Column.fromvalue(dict(datatype='string')),
        'Category',
        "specifies a) if a family-level languoid represents a pseudo-family or not; b) for "
        "language-level languoids if it belongs to a pseudo-family or is a spoken, L1 language "
        "and c) for dialect-level languoids just mirrors the level. See CodeTable for a list of "
        "all assigned categories.",
        'about/languoids.md',
        'categorical',
    ),
    'classification': ParamInfo(
        Column.fromvalue(dict(
            datatype={'base': 'string', 'format': '([a-z0-9]{4}[0-9]{4})(/[a-z0-9]{4}[0-9]{4})*'})),
        'Classification',
        'Path from root of family to the languoid as slash-separated list of Glottocodes. '
        'A NULL value for classification means the languoid is a top-level genealogical unit, '
        'i.e. an isolate or a top-level family.',
        None,
        None,
    ),
    'subclassification': ParamInfo(
        Column.fromvalue(dict(datatype={'base': 'string', 'dc:format': 'text/newick'})),
        'Subclassification',
        'Newick-formatted (sub)tree of descendants of the languoid, labeled by Glottocode',
        None,
        None,
    ),
    'med': ParamInfo(
        Column.fromvalue(dict(datatype={'base': 'integer', 'minimum': 0, 'maximum': 4})),
        'Most Extensive Description',
        'The Most Extensive Description known for a given language. See CodeTable for a '
        'description of the valid values.',
        'about/glossary.md#med',
        'sequential',
    ),
    'medovertime': ParamInfo(
        Column.fromvalue(dict(datatype={
            'base': 'json', 'format': '{"type": "array", "items": {"type": "string"}}'})),
        'Most Extensive Description over time',
        'The Most Extensive Description for a given language over time.',
        None,
        None,
    ),
    'aes': ParamInfo(
        Column.fromvalue(dict(datatype={'base': 'integer', 'minimum': 1, 'maximum': 6})),
        'Agglomerated Endangerment Status',
        'Language endangerment status compiled from various sources. See CodeTable for a '
        'description of the valid values.',
        'about/glottoscope.md',
        'sequential',
    ),
    'bib': ParamInfo(
        Column.fromvalue(dict(datatype={'base': 'boolean', 'format': 'see Source|none'})),
        'Bibliography',
        "Items from Glottolog's bibliography which are linked to a languoid are referenced "
        "from the Source field of values for this parameter.",
        None,
        None,
    )
}
