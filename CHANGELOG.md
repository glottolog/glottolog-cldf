# Changelog

All notable changes to this dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [5.1] - 2024-10-29

Based on Glottolog v5.1.


## [5.0] - 2024-03-11

- Marked `LanguageTable.Language_ID` with `parentLanguageGlottocode` property to
  avoid confusion.
- Added `LanguageTable.Is_Isolate` to make this propoerty more transparent.
- Added `LanguageTable.Level` to make languoid level easier accessible.


## [4.8] - 2023-07-10

- Added `numerical_value` column to CodeTable (see https://github.com/glottolog/glottolog-cldf/issues/19)
- Fixed wrong link to zipped sources.


## [4.7] - 2022-12-05

Added columns to LanguageTable
- `Closest_ISO369P3code`: ISO 639-3 code of the languoid or an ancestor if the languoid is a dialect.
- `First_Year_Of_Documentation`: The first year that an extinct languoid was documented (in the sense that there is data that pertains to it).
- `Last_Year_Of_Documentation`: The last year that an extinct language was documented (in the sense that there is data that pertains to it).

Added derived/computed geo-coordinates to LanguageTable:
- "recursive centroids of immediate subgroups" for language subgroups,
- Coordinate of the corresponding language-level languoid for dialects without proper coordinates.

Added TreeTable component, with classification trees for all Glottolog top-level families with language-level
languoids as leafs.

The dataset now contains all Glottolog references which are related to at least one
languoid. Consequently, the resulting BibTeX file needs to be zipped in order to stay
reasonably small. `pycldf>=1.34` will deal with this transparently, for other workflows,
you might have to unzip `cldf/sources.bib.zip` "by hand" to get the pre-4.7 behaviour back.


## [4.6.1] - 2022-07-06

- Alternative names for Glottolog languoids are now available in the CLDF dataset.


## [4.6] - 2022-05-24

- Changes to classification, AES and documentation status.


## [4.5] - 2021-12-10

- Added parameter `medovertime`. See https://github.com/glottolog/glottolog-cldf/issues/4


## [4.4] - 2021-05-14

### Added

- A human-readable description of the CLDF data in [cldf/README.md](cldf/README.md).
- This CHANGELOG.


### Changed

- Values for the parameter `subclassification` now include a `;` - making them valid Newick.


### Removed

- The `numeric_value` column in CodeTable. For parameters with integer (sequential)
  values, the `value` column in ValueTable stores this value now.
  
