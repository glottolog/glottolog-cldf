# glottolog-cldf
Glottolog data as CLDF StructureDataset

[![Build Status](https://travis-ci.org/glottolog/glottolog-cldf.svg?branch=master)](https://travis-ci.org/glottolog/glottolog-cldf)


## Parameters

- Level: language, dialect or family. "language" here does not mean that it is "assertable distinct from all other known languages" nor "has served as the main means of communication of a human society", it is a feature of the dataset structure rather than linguistic criteria. 
- Category: specifies a) if a family-languoid represents a pseudo-family or not (i.e. Sign Languages, Mixed Languages, Pidgin, Artificial Languages, Bookeeping, Unattested, Unclassified and Unclassified within non-speudo-families), b) for language-languoids if it belongs to a pseudo-family (and if so which, except for "Unclassified within x") or is "Spoken_L1_language" and c) for dialect-languoids indicates "dialect" as category
- Classification: path from root of family to languoid, `/` separated Glottocodes
- Subclassification: Newick-formatted (sub)tree of descendants of languoid (semicolon at end omitted)
- Most Extensive Description - the most extensive description known for a given language (grammar most extensive)
- Agglomerated Endangerment Status -  Language endangerment status compiled from a combination of EGDIS (Ethnologue) ElCat (Endangered Languages Catalogue) and UNESCO Atlas of Languages in Danger


## Languoids

Additional languoid metadata is provided in columns of the standard `LanguageTable`:
- Glottocode
- ISO639P3code
- Latitude
- Longitude
- Macroareas
- Countries
- `Family_ID`: Glottocode of the top-level family a languoid belongs to
- `Language_ID`: Glottocde of the language-level languoid a dialect belongs to (not to be confused with "Language_ID" in values-table)

