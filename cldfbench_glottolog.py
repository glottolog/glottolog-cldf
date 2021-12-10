import pathlib
import collections

from clldutils.misc import nfilter
from clldutils.jsonlib import dump
from cldfbench import Dataset, CLDFSpec
from pycldf.sources import Source, Reference
from pycldf.dataset import GitRepository
import pyglottolog
from pyglottolog import metadata

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
            module='StructureDataset', dir=self.cldf_dir, metadata_fname='cldf-metadata.json')

    def cmd_makecldf(self, args):
        glottolog = args.glottolog.api

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
        t = ds.add_component(
            'ParameterTable',
            {
                'name': 'type',
                'datatype': {'base': 'string', 'format': 'categorical|sequential'},
                'dc:description': 'Describes the domain of the parameter',
                'default': None,
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
            }
        )
        t.common_props['dc:description'] = \
            "This table lists parameters (or aspects) of languoids that Glottolog assigns values " \
            "for, such as the languoid's position on the Glottolog classification or the " \
            "descriptive status. Refer to the `Description` column in the table for details, and " \
            "to the `datatype` columnn for information how values for the parameter should be " \
            "interpreted."
        ds.add_component('CodeTable')
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
        )
        t.common_props['dc:description'] = \
            'This table lists all Glottolog languoids, i.e. families, languages and dialects ' \
            'which are nodes in the Glottolog classification - including "non-genealogical" ' \
            'trees as described at https://glottolog.org/glottolog/glottologinformation . ' \
            'Thus, assumptions about the properties of a languoid listed here should be made ' \
            'after including associated information from ValueTable, in particular for languoid ' \
            'level and category.'
        t.aboutUrl = 'https://glottolog.org/meta/glossary#Languoid'
        ds.add_foreign_key('LanguageTable', 'Family_ID', 'LanguageTable', 'ID')
        ds.add_foreign_key('LanguageTable', 'Language_ID', 'LanguageTable', 'ID')

        ds['LanguageTable', 'Macroarea'].separator = ';'
        ds['ValueTable', 'Value'].null = ['<NA>']

        data = args.writer.objects
        for pid, pinfo in schema.PARAMETER_INFO.items():
            data['ParameterTable'].append(dict(
                ID=pid,
                Name=pinfo.name,
                type=pinfo.type,
                Description=pinfo.description,
                infoUrl=pinfo.url,
                datatype=pinfo.dt.asdict()
            ))
        for level in glottolog.languoid_levels.values():
            data['CodeTable'].append(dict(
                ID='level-{0}'.format(level.name),
                Parameter_ID='level',
                Name=level.name,
                Description=level.description,
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
            ))

        for el in sorted(glottolog.med_types.values()):
            data['CodeTable'].append(dict(
                ID='med-{0}'.format(el.id),
                Parameter_ID='med',
                Name=el.name,
                Description=el.description,
            ))

        languoids = collections.OrderedDict((lang.id, lang) for lang in glottolog.languoids())
        refs_by_languoid, refs = glottolog.refs_by_languoid(nodes=languoids)

        def get_language_id(lang):
            if lang.level == glottolog.languoid_levels.dialect:
                for _, lid, _ in reversed(lang.lineage):
                    if languoids[lid].level == glottolog.languoid_levels.language:
                        return lid

        def format_ref(ref):
            return '{0}[{1}]'.format(ref.key, ref.pages.replace(';', ',')) if ref.pages else ref.key

        for lang in languoids.values():
            data['LanguageTable'].append(dict(
                ID=lang.id,
                Name=lang.name,
                Glottocode=lang.id,
                ISO639P3code=lang.iso,
                Latitude=lang.latitude,
                Longitude=lang.longitude,
                Macroarea=[ma.name for ma in lang.macroareas],
                Countries=[c.id for c in lang.countries],
                Family_ID=lang.lineage[0][1] if lang.lineage else None,
                Language_ID=get_language_id(lang),
            ))

            sources = sorted(refs_by_languoid[lang.id], reverse=True) \
                if lang.id in refs_by_languoid else []
            med = sources[0] if sources else None
            if med:
                ds.add_sources(Source(med.type, med.id, _check_id=False, **med.fields))
            meds = []
            last_year = 10000
            for source in sources:  # go through sources from "best" to "worst"
                if source.year_int and source.year_int < last_year:  # pick the next earlier source:
                    last_year = source.year_int
                    meds.append(source)
            if meds:
                for m in meds:
                    if ';' in m.id:
                        args.log.warning('Invalid bibtex key: {}'.format(m.id))
                    ds.add_sources(Source(m.type, m.id.replace(';', ':'), _check_id=False, **m.fields))
            clf = lang.classification_comment
            if clf:
                for ref in clf.merged_refs('family') + clf.merged_refs('sub'):
                    if ref.key not in refs:
                        args.log.warning('missing reference in classification comment: {0}'.format(ref))
                        continue
                    e = refs[ref.key]
                    ds.add_sources(Source(e.type, ref.key, _check_id=False, **e.fields))

            aes_src = lang.endangerment.source.reference_id if lang.endangerment else None
            if aes_src:
                e = refs[aes_src]
                ds.add_sources(Source(e.type, aes_src, _check_id=False, **e.fields))

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
                    lang.newick_node(nodes=languoids, template="{l.id}").newick + ';',
                    Source=[format_ref(ref) for ref in clf.merged_refs('sub')] if clf else [],
                    Comment=clf.sub if clf else None,
                ),
                value(
                    lang.id,
                    'aes',
                    lang.endangerment.status.ordinal if lang.endangerment else None,
                    Comment=lang.endangerment.comment if lang.endangerment else None,
                    Source=[aes_src] if aes_src else [],
                    Code_ID='aes-{0}'.format(lang.endangerment.status.name.replace(' ', '_'))
                    if lang.endangerment else None,
                ),
                value(
                    lang.id,
                    'med',
                    med.med_type.rank if med else None,
                    Source=[med.id] if med else [],
                    Code_ID='med-{0}'.format(med.med_type.id) if med else None,
                ),
                value(
                    lang.id,
                    'medovertime',
                    [m.text() for m in meds] or None,
                    Source=[str(Reference(m.id.replace(';', ':'), str(m.year_int))) for m in meds],
                    Code_ID=None,
                )
            ]))
