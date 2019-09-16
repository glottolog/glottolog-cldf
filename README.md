# glottolog-cldf
Glottolog data as CLDF StructureDataset

[![Build Status](https://travis-ci.org/glottolog/glottolog-cldf.svg?branch=master)](https://travis-ci.org/glottolog/glottolog-cldf)


## Parameters

- Level
- Category
- Classification: `/` separated Glottocodes
- Subclassification: Newick-formatted (sub)tree of descendants of languoid
- MostExtensiveDescription
- EndangermentStatus


## Languoids

Additional languoid metadata is provided in columns of the standard `LanguageTable`:
- Glottocode
- ISO639P3code
- Latitude
- Longitude
- Macroareas
- Countries
- `Family_ID`: Glottocode of the top-level family a languoid belongs to
- `Language_ID`: Glottocde of the language-level languoid a dialect belongs to

