"""
Computing geo-coordinates for homelands of language groups as described as "md" method in
"Testing methods of linguistic homeland detection using synthetic data"
by Søren Wichmann and Taraka Rama
https://doi.org/10.1098/rstb.2020.0202
"""
import random
import typing
import decimal
import collections

try:
    import pyproj
except ImportError:
    pyproj = None

random.seed(12345)


def md(coords: typing.List[typing.Tuple[decimal.Decimal, decimal.Decimal]], geod=None)\
        -> typing.Tuple[decimal.Decimal, decimal.Decimal]:
    """
    In the third approach, abbreviated ‘md’ for ‘minimal distance’, we compute the average
    distance (as the crow flies) from each language to all the other languages. The location
    of the language that has the smallest average distance to the others is equated with the
    homeland.

    We use the `pyproj.Geod.inv` method to compute the great-circle distance between two points.

    .. seealso: https://pyproj4.github.io/pyproj/stable/api/geod.html
    """
    geod = geod or pyproj.Geod(ellps='WGS84')

    def geodist(p1, p2):
        return geod.inv(p1[1], p1[0], p2[1], p2[0])[2]

    if len(coords) == 1:
        return coords[0]

    # We shuffle the coordinates to avoid returning the first minimal-distance location in the
    # given order.
    random.shuffle(coords)
    mindist, mincoord = None, None
    for i, coord in enumerate(coords):
        dist = sum(geodist(coord, p) for j, p in enumerate(coords) if i != j)
        if (mindist is None) or (dist < mindist):
            mindist, mincoord = dist, coord
    return mincoord


def closest_iso(writer):
    pid = 'iso6393code'
    writer.objects['ParameterTable'].append(dict(
        ID=pid,
        Name="ISO 639-3 code",
        type="other",
        Description='ISO 639-3 code assigned to the languoid or one of its ancestors in the '
                    'classification (in case of dialects). See the related discussion at '
                    'https://github.com/glottolog/glottolog-cldf/issues/13',
        datatype='"string"',
        Source=[]
    ))
    iso_codes = {
        l['ID']: l['ISO639P3code'] for l in writer.objects['LanguageTable'] if l['ISO639P3code']}
    for v in writer.objects['ValueTable']:
        if v['Parameter_ID'] == 'classification':
            gc = v['Language_ID']
            for code in [gc] + list(reversed(v['Value'].split('/'))):
                if code in iso_codes:
                    writer.objects['ValueTable'].append(dict(
                        ID='{}-{}'.format(gc, pid),
                        Language_ID=gc,
                        Parameter_ID=pid,
                        Value=iso_codes[code],
                    ))
                    break


def homelands(writer):
    pid = 'homeland'
    writer.objects['ParameterTable'].append(dict(
        ID=pid,
        Name="homeland",
        type="other",
        Description='Geocoordinate of the "homeland" of a language group computed using the '
                    '"minimal distance" method from '
                    '[Wichmann and Rama 2021](https://doi.org/10.1098/rstb.2020.0202), '
                    'serialized as JSON array specifying latitude and longitude. '
                    'Please cite Wichmann and Rama 2021, if you use this data.',
        datatype='"json"',
        Source=['Wichmann2021']
    ))
    writer.cldf.add_sources("""
@article{Wichmann2021,
  doi = {10.1098/rstb.2020.0202},
  url = {https://doi.org/10.1098/rstb.2020.0202},
  year = {2021},
  publisher = {The Royal Society},
  volume = {376},
  number = {1824},
  author = {Søren Wichmann and Taraka Rama},
  title = {Testing methods of linguistic homeland detection using synthetic data},
  journal = {Philosophical Transactions of the Royal Society B: Biological Sciences}
}
    """)
    vals = [
        v for v in writer.objects['ValueTable'] if v['Parameter_ID'] in ['level', 'classification']]

    # Find language-level languoids with coordinates:
    languages = {
        v['Language_ID'] for v in vals
        if v['Parameter_ID'] == 'level' and v['Code_ID'] == 'level-language'}
    languages_with_coords = {
        l['ID']: (l['Latitude'], l['Longitude']) for l in writer.objects['LanguageTable']
        if l['ID'] in languages and l['Latitude'] is not None}

    # Collect sets of languages per language family/subgroup:
    subgroups = collections.defaultdict(list)
    for v in vals:
        if (v['Language_ID'] in languages_with_coords) and (v['Parameter_ID'] == 'classification'):
            for gc in v['Value'].split('/'):
                subgroups[gc].append(languages_with_coords[v['Language_ID']])

    # Compute minimal distances per group:
    g = pyproj.Geod(ellps='WGS84')
    for group, coords in sorted(subgroups.items(), key=lambda i: i[0]):
        writer.objects['ValueTable'].append(dict(
            ID='{}-{}'.format(group, pid),
            Language_ID=group,
            Parameter_ID=pid,
            Value='[{},{}]'.format(*md(coords, g)),
        ))
