# Changelog

All notable changes to this dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [Unreleased]


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
  
