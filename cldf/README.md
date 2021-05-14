<a name="ds-cldfmetadatajson"> </a>

# StructureDataset glottolog/glottolog: Glottolog database 4.4 as CLDF

**CLDF Metadata**: [cldf-metadata.json](./cldf-metadata.json)

**Sources**: [sources.bib](./sources.bib)

Comprehensive reference information for the world's languages, especially the lesser known languages

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian. 2021. Glottolog 4.4. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://glottolog.org)
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF StructureDataset](http://cldf.clld.org/v1.0/terms.rdf#StructureDataset)
[dc:identifier](http://purl.org/dc/terms/identifier) | https://glottolog.org
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/glottolog/glottolog-cldf
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/glottolog/glottolog-cldf/tree/22b4043">glottolog/glottolog-cldf v4.3-8-g22b4043</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v4.4">Glottolog v4.4</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><a href="https://github.com/glottolog/pyglottolog/tree/3.5.0">glottolog/pyglottolog 3.5.0</a></li><li><strong>python</strong>: 3.8.5</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | glottolog
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-valuescsv"></a>Table [values.csv](./values.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ValueTable](http://cldf.clld.org/v1.0/terms.rdf#ValueTable)
[dc:extent](http://purl.org/dc/terms/extent) | 155400


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Code_ID](http://cldf.clld.org/v1.0/terms.rdf#codeReference) | `string` | References [codes.csv::ID](#table-codescsv)
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`codeReference` | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

This table lists parameters (or aspects) of languoids that Glottolog assigns values for, such as the languoid's position on the Glottolog classification or the descriptive status. Refer to the `Description` column in the table for details, and to the `datatype` columnn for information how values for the parameter should be interpreted.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 6


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
`type` | `string` | Describes the domain of the parameter
`infoUrl` | `string` | URL (relative to `aboutUrl`) of a web page with further information about the parameter
`datatype` | `json` | CSVW datatype description for values for this parameter. I.e. content of the Value column of associated rows in ValueTable should be interpreted/parsed accordingly

## <a name="table-codescsv"></a>Table [codes.csv](./codes.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF CodeTable](http://cldf.clld.org/v1.0/terms.rdf#CodeTable)
[dc:extent](http://purl.org/dc/terms/extent) | 29


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

This table lists all Glottolog languoids, i.e. families, languages and dialects which are nodes in the Glottolog classification - including "non-genealogical" trees as described at https://glottolog.org/glottolog/glottologinformation . Thus, assumptions about the properties of a languoid listed here should be made after including associated information from ValueTable, in particular for languoid level and category.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 25900


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | list of `string` (separated by `;`) | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal` | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
[Countries](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) | list of `string` (separated by `;`) | ISO 3166-1 alpha-2 country codes for countries a language is spoken in.
`Family_ID` | `string` | Glottocode of the top-level genetic unit, the languoid belongs to<br>References [languages.csv::ID](#table-languagescsv)
`Language_ID` | `string` | Glottocode of the language-level languoid, the languoid belongs to (in case of dialects)<br>References [languages.csv::ID](#table-languagescsv)

