# glottolog/glottolog: Glottolog database 4.6 as CLDF

[![CLDF validation](https://github.com/glottolog/glottolog-cldf/workflows/CLDF-validation/badge.svg)](https://github.com/glottolog/glottolog-cldf/actions?query=workflow%3ACLDF-validation)

## How to cite

If you use these data please cite
- the original source
  > Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian. 2022. Glottolog 4.6. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://glottolog.org)
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


Comprehensive reference information for the world's languages, especially the lesser known languages

This dataset is licensed under a CC-BY-4.0 license

Available online at https://glottolog.org

### Parameters
In addition to the langoid metadata in the [LanguageTable](cldf#table-languagescsv) this dataset contains values for the following [parameters](cldf#table-parameterscsv).

ID | Name | Description | Source
--- | --- | --- | ---
level | Level | Languoid level information needs to be interpreted in the context of the languoid's category. For languoids in 'non-genealogical trees' as described in https://glottolog.org/glottolog/glottologinformation the principles for determining language level languoids (see https://glottolog.org/glottolog/glottologinformation#principles) do not hold. Instead, in these cases, 'family' just means 'group of languoids', 'language' means 'languoid with extended metadata such as coordinates', and 'dialect' mean any type of 'sub-lect'. | 
category | Category | specifies a) if a family-level languoid represents a pseudo-family or not; b) for language-level languoids if it belongs to a pseudo-family or is a spoken, L1 language and c) for dialect-level languoids just mirrors the level. See CodeTable for a list of all assigned categories. | 
classification | Classification | Path from root of family to the languoid as slash-separated list of Glottocodes. A NULL value for classification means the languoid is a top-level genealogical unit, i.e. an isolate or a top-level family. | 
subclassification | Subclassification | Newick-formatted (sub)tree of descendants of the languoid, labeled by Glottocode | 
med | Most Extensive Description | The Most Extensive Description known for a given language. See CodeTable for a description of the valid values. | 
medovertime | Most Extensive Description over time | The Most Extensive Description for a given language over time. | 
aes | Agglomerated Endangerment Status | Language endangerment status compiled from various sources. See CodeTable for a description of the valid values. | 
iso6393code | ISO 639-3 code | ISO 639-3 code assigned to the languoid or one of its ancestors in the classification (in case of dialects). See the related discussion at https://github.com/glottolog/glottolog-cldf/issues/13 | 
homeland | homeland | Geocoordinate of the "homeland" of a language group computed using the "minimal distance" method from [Wichmann and Rama 2021](https://doi.org/10.1098/rstb.2020.0202), serialized as JSON array specifying latitude and longitude. Please cite Wichmann and Rama 2021, if you use this data. | Wichmann, Søren and Rama, Taraka. 2021. Testing methods of linguistic homeland detection using synthetic data. Philosophical Transactions of the Royal Society B: Biological Sciences 376. The Royal Society.


## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [StructureDataset](https://github.com/cldf/cldf/tree/master/modules/StructureDataset) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)