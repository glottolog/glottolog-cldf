from collections import namedtuple

from csvw.metadata import Datatype

ParamInfo = namedtuple('ParamInfo', 'dt name description url type')

PARAMETER_INFO = {
    'level': ParamInfo(
        Datatype.fromvalue(dict(base='string', format='family|language|dialect')),
        'Level',
        "Languoid level information needs to be interpreted in the context of the languoid's "
        "category. For languoids in 'non-genealogical trees' as described in "
        "https://glottolog.org/glottolog/glottologinformation the principles for determining "
        "language level languoids "
        "(see https://glottolog.org/glottolog/glottologinformation#principles) do not hold. "
        "Instead, in these cases, 'family' just means 'group of languoids', 'language' means "
        "'languoid with extended metadata such as coordinates', and 'dialect' mean any type of "
        "'sub-lect'.",
        'meta/glossary#Languoid',
        'categorical',
    ),
    'category': ParamInfo(
        Datatype.fromvalue('string'),
        'Category',
        "specifies a) if a family-level languoid represents a pseudo-family or not; b) for "
        "language-level languoids if it belongs to a pseudo-family or is a spoken, L1 language "
        "and c) for dialect-level languoids just mirrors the level. See CodeTable for a list of "
        "all assigned categories.",
        'glottolog/glottologinformation',
        'categorical',
    ),
    'classification': ParamInfo(
        Datatype.fromvalue(
            {'base': 'string', 'format': '([a-z0-9]{4}[0-9]{4})(/[a-z0-9]{4}[0-9]{4})*'}),
        'Classification',
        'Path from root of family to the languoid as slash-separated list of Glottocodes. '
        'A NULL value for classification means the languoid is a top-level genealogical unit, '
        'i.e. an isolate or a top-level family.',
        None,
        None,
    ),
    'subclassification': ParamInfo(
        Datatype.fromvalue({'base': 'string', 'dc:format': 'text/newick'}),
        'Subclassification',
        'Newick-formatted (sub)tree of descendants of the languoid, labeled by Glottocode',
        None,
        None,
    ),
    'med': ParamInfo(
        Datatype.fromvalue({'base': 'integer', 'minimum': 0, 'maximum': 4}),
        'Most Extensive Description',
        'The Most Extensive Description known for a given language. See CodeTable for a '
        'description of the valid values.',
        'meta/glossary#sec-mostextensivedescriptionmed',
        'sequential',
    ),
    'aes': ParamInfo(
        Datatype.fromvalue({'base': 'integer', 'minimum': 1, 'maximum': 6}),
        'Agglomerated Endangerment Status',
        'Language endangerment status compiled from various sources. See CodeTable for a '
        'description of the valid values.',
        'langdoc/status',
        'sequential',
    )
}
