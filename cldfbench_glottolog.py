import re
import pathlib
import collections

from tqdm import tqdm
from clldutils.misc import nfilter
from clldutils.jsonlib import dump
from cldfbench import Dataset, CLDFSpec
from pycldf.sources import Source, Reference
from pycldf.dataset import GitRepository
import pyglottolog
from pyglottolog import metadata
from pyglottolog import homelands
from pyglottolog.references import BibFile
import nexus
from nexus.handlers.tree import Tree as NexusTree

import schema


def value(lid, pid, value, **kw):
    if value is None:
        return
    res = dict(
        ID='{0}-{1}'.format(lid, pid),
        Language_ID=lid,
        Parameter_ID=pid,
        Value=value,
    )
    res.update(**kw)
    return res


def repos(name, **kw):
    return GitRepository('https://github.com/glottolog/{0}'.format(name), **kw)


class GlottologDataset(Dataset):
    id = 'glottolog'
    dir = pathlib.Path(__file__).parent

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(
            module='StructureDataset',
            dir=self.cldf_dir,
            zipped=['Source'],
            metadata_fname='cldf-metadata.json')

    def cmd_readme(self, args):
        params = [
            '\n### Parameters\n'
            'In addition to the langoid metadata in the [LanguageTable]({0}#table-languagescsv) '
            'this dataset contains values for the following '
            '[parameters]({0}#table-parameterscsv).\n'.format(
                self.cldf_dir.resolve().relative_to(self.dir.resolve())),
            'ID | Name | Description',
            '--- | --- | ---'
        ]
        for p in self.cldf_reader().objects('ParameterTable'):
            params.append(' | '.join([
                p.id,
                p.cldf.name,
                p.cldf.description,
            ]))
        return super().cmd_readme(args) + '\n'.join(params) + '\n'

    def cmd_makecldf(self, args):
        glottolog = args.glottolog.api
        hl = homelands.compute(glottolog, homelands.recursive_centroids)
        contrib = ["""\
# Contributors

name | affiliation | orcid | github | role
---  | ----------- | ----- | ------ | ----"""]
        for ed in glottolog.current_editors:
            contrib.append(' | '.join(
                [ed.name, ed.affiliation, ed.orcid, '@' + getattr(ed, 'github'), 'maintainer']))
        self.dir.joinpath('CONTRIBUTORS.md').write_text('\n'.join(contrib), encoding='utf8')

        # write metadata.json
        dump(
            {
                "title": glottolog.publication.zenodo.title_format.format(
                    glottolog.publication.zenodo.version) + ' as CLDF',
                "citation": metadata.citation(glottolog),
                "url": glottolog.publication.web.url,
                "description": glottolog.publication.web.description,
                "id": "glottolog",
                "license": glottolog.publication.zenodo.license_id,
            },
            self.dir / 'metadata.json',
            indent=4,
        )

        ds = args.writer.cldf
        ds.add_provenance(
            wasGeneratedBy=repos('pyglottolog', version=pyglottolog.__version__),
        )
        self.schema(ds)
        data = args.writer.objects
        for pid, pinfo in schema.PARAMETER_INFO.items():
            data['ParameterTable'].append(dict(
                ID=pid,
                Name=pinfo.name,
                type=pinfo.type,
                Description=pinfo.description,
                infoUrl=pinfo.url,
                datatype=pinfo.dt.asdict(),
                Source=[],
            ))
        for level in glottolog.languoid_levels.values():
            data['CodeTable'].append(dict(
                ID='level-{0}'.format(level.name),
                Parameter_ID='level',
                Name=level.name,
                Description=level.description,
                numerical_value=level.ordinal,
            ))
            data['CodeTable'].append(dict(
                ID='category-{0}'.format(level.name.capitalize()),
                Parameter_ID='category',
                Name=level.name.capitalize()))
            data['CodeTable'].append(dict(
                ID='category-Pseudo_{0}'.format(level.name.capitalize()),
                Parameter_ID='category',
                Name='Pseudo {}'.format(level.name.capitalize())))

        for el in sorted(glottolog.language_types.values()):
            data['CodeTable'].append(dict(
                ID='category-{0}'.format(el.category.replace(' ', '_')),
                Parameter_ID='category',
                Name=el.category))

        for el in sorted(glottolog.aes_status.values()):
            data['CodeTable'].append(dict(
                ID='aes-{0}'.format(el.name.replace(' ', '_')),
                Parameter_ID='aes',
                Name=el.name,
                Description='EGIDS: {0.egids}; UNESCO: {0.unesco}; ElCat: {0.unesco}'.format(el),
                numerical_value=el.ordinal,
            ))

        for el in sorted(glottolog.med_types.values()):
            data['CodeTable'].append(dict(
                ID='med-{0}'.format(el.id),
                Parameter_ID='med',
                Name=el.name,
                Description=el.description,
                numerical_value=el.rank,
            ))

        srcids = set()

        def add_src(e):
            e.fields['citekeys'] = e.fields.pop('srctrickle').replace('#', ':')
            srcids.add(e.fields['glottolog_ref_id'])
            ds.add_sources(Source(e.type, e.fields['glottolog_ref_id'], _check_id=False, **e.fields))

        languoids = collections.OrderedDict((lang.id, lang) for lang in glottolog.languoids())
        lbc = glottolog.languoids_by_code(languoids)
        refs_by_languoid, refs = collections.defaultdict(list), {}
        for e in BibFile(fname=glottolog.build_path('monster-utf8.bib'), api=glottolog).iterentries():
            refs[e.fields['glottolog_ref_id']] = e
            for t in e.fields['srctrickle'].split(', '):
                refs[t.replace('#', ':')] = e

            for i, lang in enumerate(e.languoids(lbc)[0]):  # ignore computerized assignment!
                if i == 0:
                    add_src(e)
                refs_by_languoid[lang.id].append(e.fields['glottolog_ref_id'])

        def get_language_id(lang):
            if lang.level == glottolog.languoid_levels.dialect:
                for _, lid, _ in reversed(lang.lineage):
                    if languoids[lid].level == glottolog.languoid_levels.language:
                        return lid

        def format_ref(ref):
            e = refs[getattr(ref, 'key', ref)]
            eid = e.fields['glottolog_ref_id']
            if eid not in srcids:
                add_src(e)
            return '{0}[{1}]'.format(eid, ref.pages.replace(';', ',')) if getattr(ref, 'pages', None) else eid

        nns = {}  # Cache newick nodes!
        ncount = 0
        lcoords = {}
        nex = nexus.NexusWriter()

        for lang in tqdm(sorted(languoids.values(), key=lambda lg: len(lg.lineage))):
            nn = nns.get(lang.id)
            if not nn:
                nn = lang.newick_node(nodes=languoids, template="{l.id}")
                for node in nn.walk():
                    nns[node.name] = node

            if lang.level == glottolog.languoid_levels.language:
                lcoords[lang.id] = (lang.latitude, lang.longitude)

            if len(lang.lineage) == 0 and lang.level == glottolog.languoid_levels.family:
                args.writer.objects['TreeTable'].append(dict(
                    ID=lang.id,
                    Name=lang.id,
                    Description='Glottolog classification of the languages in the family {}'.format(lang.name),
                    Media_ID='classification',
                ))
                nex.trees.append(NexusTree.from_newick(
                    lang.newick_node(
                        nodes=languoids,
                        template="{l.id}",
                        maxlevel=glottolog.languoid_levels.language),
                    name=lang.id,
                    rooted=True))

            lid = get_language_id(lang)
            latlon = (lang.latitude, lang.longitude)
            if lang.latitude is None:
                if lang.id in hl:
                    latlon = hl[lang.id]
                elif lid in lcoords:
                    latlon = lcoords[lid]

            timespan = list(lang.timespan or (None, None))
            if timespan[0] == timespan[1]:
                timespan[0] = None
            if timespan[1]:
                assert lang.endangerment.status == glottolog.aes_status.extinct
            data['LanguageTable'].append(dict(
                ID=lang.id,
                Name=lang.name,
                Glottocode=lang.id,
                ISO639P3code=lang.iso,
                Latitude=latlon[0],
                Longitude=latlon[1],
                Macroarea=[ma.name for ma in lang.macroareas],
                Countries=[c.id for c in lang.countries],
                Family_ID=lang.lineage[0][1] if lang.lineage else None,
                Language_ID=lid,
                Closest_ISO369P3code=lang.closest_iso(nodes=languoids),
                First_Year_Of_Documentation=timespan[0],
                Last_Year_Of_Documentation=timespan[1],
            ))
            for prov, names in sorted(lang.names.items(), key=lambda i: i[0]):
                if prov != 'hhbib_lgcode':
                    for name in sorted(names):
                        lcode = ''
                        match = re.search(r'\s*\[([a-z]+)]$', name)
                        if match:
                            lcode = match.groups()[0]
                            name = name[:match.start()]
                        ncount += 1
                        data['names.csv'].append(dict(
                            ID=str(ncount),
                            Language_ID=lang.id,
                            Name=name,
                            Provider=prov,
                            lang=lcode,
                        ))

            #if ncount > 1000:
            #    break

            sources = sorted([refs[k] for k in refs_by_languoid[lang.id]], reverse=True) \
                if lang.id in refs_by_languoid else []
            med = sources[0] if sources else None
            meds = []
            last_year = 10000
            for source in sources:  # go through sources from "best" to "worst"
                if source.year_int and source.year_int < last_year:  # pick the next earlier source:
                    last_year = source.year_int
                    meds.append(source)
            clf = lang.classification_comment
            if clf:
                for ref in clf.merged_refs('family') + clf.merged_refs('sub'):
                    if ref.key not in refs:
                        args.log.warning('missing reference in classification comment: {0}'.format(ref))
                        continue

            aes_src = lang.endangerment.source.reference_id if lang.endangerment else None
            data['ValueTable'].extend(nfilter([
                value(
                    lang.id,
                    'level',
                    lang.level.name,
                    Code_ID='level-{0}'.format(lang.level.name)),
                value(
                    lang.id,
                    'category',
                    lang.category.replace(' ', '_'),
                    Code_ID='category-{0}'.format(lang.category.replace(' ', '_')),
                ),
                value(
                    lang.id,
                    'classification',
                    schema.PARAMETER_INFO['classification'].dt.formatted(
                        '/'.join([li[1] for li in lang.lineage])) or None,
                    Source=[format_ref(ref) for ref in clf.merged_refs('family')] if clf else [],
                    Comment=clf.family if clf else None,
                ),
                value(
                    lang.id,
                    'subclassification',
                    nn.newick + ';',
                    Source=[format_ref(ref) for ref in clf.merged_refs('sub')] if clf else [],
                    Comment=clf.sub if clf else None,
                ),
                value(
                    lang.id,
                    'aes',
                    lang.endangerment.status.ordinal if lang.endangerment else None,
                    Comment=lang.endangerment.comment if lang.endangerment else None,
                    Source=[format_ref(aes_src)] if aes_src else [],
                    Code_ID='aes-{0}'.format(lang.endangerment.status.name.replace(' ', '_'))
                    if lang.endangerment else None,
                ),
                value(
                    lang.id,
                    'med',
                    med.med_type.rank if med else None,
                    Source=[med.fields['glottolog_ref_id']] if med else [],
                    Code_ID='med-{0}'.format(med.med_type.id) if med else None,
                ),
                value(
                    lang.id,
                    'medovertime',
                    [m.text() for m in meds] or None,
                    Source=[str(Reference(m.fields['glottolog_ref_id'], str(m.year_int))) for m in meds],
                    Code_ID=None,
                )
            ]))

        nex.write_to_file(args.writer.cldf_spec.dir / 'classification.nex')
        args.writer.objects['MediaTable'].append(dict(
            ID='classification',
            Media_Type='text/plain',
            Download_URL='classification.nex',
        ))

    def schema(self, ds):
        t = ds.add_component(
            'ParameterTable',
            {
                'name': 'type',
                'datatype': {'base': 'string', 'format': 'categorical|sequential|other'},
                'dc:description': 'Describes the domain of the parameter',
                #'default': None,
            },
            {
                'name': 'infoUrl',
                'dc:description': 'URL (relative to `aboutUrl`) of a web page with further '
                                  'information about the parameter',
                'aboutUrl': 'https://glottolog.org/{+infoUrl}',
            },
            {
                'name': 'datatype',
                'datatype': 'json',
                'dc:description':
                    'CSVW datatype description for values for this parameter. I.e. content of the '
                    'Value column of associated rows in ValueTable should be interpreted/parsed '
                    'accordingly',
            },
            {
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source",
                "name": "Source",
                "separator": ";",
                "dc:description": "Source describing the parameter in detail"
            }
        )
        t.common_props['dc:description'] = \
            "This table lists parameters (or aspects) of languoids that Glottolog assigns values " \
            "for, such as the languoid's position on the Glottolog classification or the " \
            "descriptive status. Refer to the `Description` column in the table for details, and " \
            "to the `datatype` columnn for information how values for the parameter should be " \
            "interpreted."
        ds.add_component(
            'CodeTable',
            {
                "name": "numerical_value",
                "datatype": "integer",
                "dc:description":
                    "Integer value associated with a code. Implements ordering for ordered "
                    "parameter domains.",
            }
        )
        ds.add_columns('ValueTable', 'codeReference')
        t = ds.add_component(
            'LanguageTable',
            {
                'name': 'Countries',
                'separator': ';',
                'dc:description':
                    'ISO 3166-1 alpha-2 country codes for countries a language is spoken in.',
                'propertyUrl': 'https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2',
                'aboutUrl': 'https://en.wikipedia.org/wiki/ISO_3166-2:{Countries}',
            },
            {
                'name': 'Family_ID',
                'dc:description':
                    'Glottocode of the top-level genetic unit, the languoid belongs to'},
            {
                'name': 'Language_ID',
                'dc:description':
                    'Glottocode of the language-level languoid, the languoid belongs to '
                    '(in case of dialects)'},
            {
                'name': 'Closest_ISO369P3code',
                'dc:description':
                    "ISO 639-3 code of the languoid or an ancestor if the languoid is a dialect. "
                    "See also https://github.com/glottolog/glottolog-cldf/issues/13",
            },
            {
                'name': 'First_Year_Of_Documentation',
                'datatype': 'integer',
                'dc:description':
                    "The first year that an extinct languoid was documented (in the "
                    "sense that there is data that pertains to it). "
                    "Positive numbers are years AD, negative numbers are years BC.",
            },
            {
                'name': 'Last_Year_Of_Documentation',
                'datatype': 'integer',
                'dc:description':
                    "The last year that an extinct language was documented.  (in the "
                    "sense that there is data that pertains to it). "
                    "Positive numbers are years AD, negative numbers are years BC.",
            }
        )
        t.common_props['dc:description'] = \
            'This table lists all Glottolog languoids, i.e. families, languages and dialects ' \
            'which are nodes in the Glottolog classification - including "non-genealogical" ' \
            'trees as described at https://glottolog.org/glottolog/glottologinformation . ' \
            'Thus, assumptions about the properties of a languoid listed here should be made ' \
            'after including associated information from ValueTable, in particular for languoid ' \
            'level and category. Locations (WGS 84 coordinates) for language groups, i.e. ' \
            'languoids of level "family are computed as recursive centroids as described at ' \
            'https://pyglottolog.readthedocs.io/en/latest/homelands.html' \
            '#pyglottolog.homelands.recursive_centroids while locations for dialects are simply ' \
            'inherited from the associated languoids of level "language" in most cases.'
        t.aboutUrl = 'https://glottolog.org/meta/glossary#Languoid'
        ds.add_foreign_key('LanguageTable', 'Family_ID', 'LanguageTable', 'ID')
        ds.add_foreign_key('LanguageTable', 'Language_ID', 'LanguageTable', 'ID')

        ds['LanguageTable', 'Macroarea'].separator = ';'
        ds['ValueTable', 'Value'].null = ['<NA>']

        t = ds.add_table(
            'names.csv',
            {
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
                "name": "ID"
            },
            {
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#languageReference",
                "name": "Language_ID"
            },
            {
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name",
                "name": "Name"
            },
            {
                "propertyUrl": "http://purl.org/dc/terms/source",
                "name": "Provider",
            },
            {
                "propertyUrl": "http://purl.org/dc/elements/1.1/language",
                "name": "lang",
            },
        )
        t.common_props['dc:description'] = \
            "Alternative names for Glottolog languoids  from various sources."
        ds.add_component('TreeTable')
        ds.add_component('MediaTable')
