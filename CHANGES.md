## Changes

### 0.11.0 (2021-04-12)

- **Refactored, standardized, and extended several areas of functionality**
  - text preprocessing (`textacy.preprocessing`)
    - Added functions for normalizing bullet points in lists (`normalize.bullet_points()`), removing HTML tags (`remove.html_tags()`), and removing bracketed contents such as in-line citations (`remove.brackets()`).
    - Added `make_pipeline()` function for combining multiple preprocessors applied sequentially to input text into a single callable.
    - Renamed functions for flexibility and clarity of use; in most cases, this entails replacing an underscore with a period, e.g. `preprocessing.normalize_whitespace()` => `preprocessing.normalize.whitespace()`.
    - Renamed and standardized some funcs' args; for example, all "replace" functions had their (optional) second argument renamed from `replace_with` => `repl`, and `remove.punctuation(text, marks=".?!")` => `remove.punctuation(text, only=[".", "?", "!"])`.
  - structured information extraction (`textacy.extract`)
    - Consolidated and restructured functionality previously spread across the `extract.py` and `text_utils.py` modules and `ke` subpackage. For the latter two, imports have changed:
      - `from textacy import ke; ke.textrank()` => `from textacy import extract; extract.keyterms.textrank()`
      - `from textacy import text_utils; text_utils.keywords_in_context()` => `from textacy import extract; extract.keywords_in_context()`
    - Added new extraction functions:
      - `extract.regex_matches()`: For matching regex patterns in a document's text that cross spaCy token boundaries, with various options for aligning matches back to tokens.
      - `extract.acronyms()`: For extracting acronym-like tokens, without looking around for related definitions.
      - `extract.terms()`: For flexibly combining n-grams, entities, and noun chunks into a single collection, with optional deduplication.
    - Improved the generality and quality of extracted "triples" such as Subject-Verb-Objects, and changed the structure of returned objects accordingly. Previously, only contiguous spans were permitted for each element, but this was overly restrictive: A sentence like "I did not really like the movie." would produce an SVO of `("I", "like", "movie")` which is... misleading. The new approach uses lists of tokens that need not be adjacent; in this case, it produces `(["I"], ["did", "not", "like"], ["movie"])`. For convenience, triple results are all named tuples, so elements may be accessed by name or index (e.g. `svo.subject` == `svo[0]`).
    - Changed `extract.keywords_in_context()` to always yield results, with optional padding of contexts, leaving printing of contexts up to users; also extended it to accept `Doc` or `str` objects as input.
    - Removed deprecated `extract.pos_regex_matches()` function, which is superseded by the more powerful `extract.token_matches()`.
  - string and sequence similarity metrics (`textacy.similarity`)
    - Refactored top-level `similarity.py` module into a subpackage, with metrics split out into categories: edit-, token-, and sequence-based approaches, as well as hybrid metrics.
    - Added several similarity metrics:
      - edit-based Jaro (`similarity.jaro()`)
      - token-based Cosine (`similarity.cosine()`), Bag (`similarity.bag()`), and Tversky (`similarity.tvserky()`)
      - sequence-based Matching Subsequences Ratio (`similarity.matching_subsequences_ratio()`)
      - hybrid Monge-Elkan (`similarity.monge_elkan()`)
    - Removed a couple similarity metrics: Word Movers Distance relied on a troublesome external dependency, and Word2Vec+Cosine is available in spaCy via `Doc.similarity`.
  - network- and vector-based document representations (`textacy.representations`)
    - Consolidated and reworked networks functionality in `representations.network` module
      - Added `build_cooccurrence_network()` function to represent a sequence of strings (or a sequence of such sequences) as a graph with nodes for each unique string and edges to other strings that co-occurred.
      - Added `build_similarity_network()` function to represent a sequence of strings (or a sequence of such sequences) as a graph with nodes as top-level elements and edges to all others weighted by pairwise similarity.
      - Removed obsolete `network.py` module and duplicative `extract.keyterms.graph_base.py` module.
    - Refined vectorizer initialization, and moved from `vsm.vectorizers` to `representations.vectorizers` module.
      - For both `Vectorizer` and `GroupVectorizer`, applying global inverse document frequency weights is now handled by a single arg: `idf_type: Optional[str]`, rather than a combination of `apply_idf: bool, idf_type: str`; similarly, applying document-length weight normalizations is handled by `dl_type: Optional[str]` instead of `apply_dl: bool, dl_type: str`
    - Added `representations.sparse_vec` module for higher-level access to document vectorization via `build_doc_term_matrix()` and `build_grp_term_matrix()` functions, for cases when a single fit+transform is all you need.
  - automatic language identification (`textacy.lang_id`)
    - Moved functionality from `lang_utils.py` module into a subpackage, and added the primary user interface (`identify_lang()` and `identify_topn_langs()`) as package-level imports.
    - Implemented and trained a more accurate `thinc`-based language identification model that's closer to the original CLD3 inspiration, replacing the simpler `sklearn`-based pipeline.
- **Updated interface with spaCy for v3, and better leveraged the new functionality**
  - Restricted `textacy.load_spacy_lang()` to only accept full spaCy language pipeline names or paths, in accordance with v3's removal of pipeline aliases and general tightening-up on this front. Unfortunately, `textacy` can no longer play fast and loose with automatic language identification => pipeline loading...
  - Extended `textacy.make_spacy_doc()` to accept a `chunk_size` arg that splits input text into chunks, processes each individually, then joins them into a single `Doc`; supersedes `spacier.utils.make_doc_from_text_chunks()`, which is now deprecated.
  - Moved core `Doc` extensions into a top-level `extensions.py` module, and improved/streamlined the collection
    - Refactored and improved performance of `Doc._.to_bag_of_words()` and `Doc._.to_bag_of_terms()`, leveraging related functionality in `extract.words()` and `extract.terms()`
    - Removed redundant/awkward extensions:
      - `Doc._.lang` => use `Doc.lang_`
      - `Doc._.tokens` => use `iter(Doc)`
      - `Doc._.n_tokens` => `len(Doc)`
      - `Doc._.to_terms_list()` => `extract.terms(doc)` or `Doc._.extract_terms()`
      - `Doc._.to_tagged_text()` => NA, this was an old holdover that's not used in practice anymore
      - `Doc._.to_semantic_network()` => NA, use a function in `textacy.representations.networks`
  - Added `Doc` extensions for `textacy.extract` functions (see above for details), with most functions having direct analogues; for example, to extract acronyms, use either `textacy.extract.acronyms(doc)` or `doc._.extract_acronyms()`. Keyterm extraction functions share a single extension: `textacy.extract.keyterms.textrank(doc)` <> `doc._.extract_keyterms(method="textrank")`
  - Leveraged spaCy's new `DocBin` for efficiently saving/loading `Doc`s in binary format, with corresponding arg changes in `io.write_spacy_docs()` and `Corpus.save()`+`.load()`
- **Improved package documentation, tests, dependencies, and type annotations**
  - Added two beginner-oriented tutorials to documentation, showing how to use various aspects of the package in the context of specific tasks.
  - Reorganized API reference docs to put like functionality together and more consistently provide summary tables up top
  - Updated dependencies list and package versions
    - Removed: `pyemd` and `srsly`
    - Un-capped max versions: `numpy` and `scikit-learn`
    - Bumped min versions: `cytoolz`, `jellyfish`, `matplotlib`, `pyphen`, and `spacy` (v3.0+ only!)
  - Bumped min Python version from 3.6 => 3.7, and added PY3.9 support
  - Removed `textacy.export` module, which had functions for exporting spaCy docs into other external formats; this was a soft dependency on `gensim` and CONLL-U that wasn't enforced or guaranteed, so better to remove.
  - Added `types.py` module for shared types, and used them everywhere. Also added/fixed type annotations throughout the code base.
  - Improved, added, and parametrized literally hundreds of tests.

#### Contributors

Many thanks to @timgates42, @datanizing, @8W9aG, @0x2b3bfa0, and @gryBox for submitting PRs, either merged or used as inspiration for my own rework-in-progress.


### 0.10.1 (2020-08-29)

#### New and Changed:

- **Expanded text statistics and refactored into a sub-package (PR #307)**
  - Refactored `text_stats` module into a sub-package with the same name and top-level API, but restructured under the hood for better consistency
  - Improved performance, API, and documentation on the main `TextStats` class, and improved documentation on many of the individual stats functions
  - Added new readability tests for texts in Arabic (Automated Arabic Readability Index), Spanish (µ-legibility and perspecuity index), and Turkish (a lang-specific formulation of Flesch Reading Ease)
  - _Breaking change:_ Removed `TextStats.basic_counts` and `TextStats.readability_stats` attributes, since typically only one or a couple needed for a given use case; also, some of the readability tests are language-specific, which meant bad results could get mixed in with good ones
- **Improved and standardized some code quality and performance (PR #305, #306)**
  - Standardized error messages via top-level `errors.py` module
  - Replaced `str.format()` with f-strings (almost) everywhere, for performance and readability
  - Fixed a whole mess of linting errors, significantly improving code quality and consistency
- **Improved package configuration, and maintenance (PRs #298, #305, #306)**
  - Added automated GitHub workflows for building and testing the package, linting and formatting, publishing new releases to PyPi, and building documentation (and ripped out Travis CI)
  - Added a makefile with common commands for dev work, plus instructions
  - Adopted the new `pyproject.toml` package configuration standard; updated and streamlined `setup.py` and `setup.cfg` accordingly; and removed `requirements.txt`
  - Moved all source code into a `/src` directory, for technical reasons
  - Added `mypy`-specific config file to reduce output noisiness when type-checking
- **Improved and moved package documentation (PR #309)**
  - Moved the docs site back to ReadTheDocs (https://textacy.readthedocs.io)! Pardon the years-long detour into GitHub Pages...
  - Enabled markdown-based documentation using `recommonmark` instead of `m2r`, and migrated all "narrative" docs from `.rst` to equivalent `.md` files
  - Added auto-generated summary tables to many sections of the API Reference, to help users get an overview of functionality and better find what they're looking for; also added auto-generated section heading references
  - Tidied up and further standardized docstrings throughout the code
- **Kept up with the Python ecosystem**
  - Trained a v1.1 language identifier model using `scikit-learn==0.23.0`, and bumped the upper bound on that dependency's version accordingly
  - Updated and parametrized many tests using modern `pytest` functionality (PR #306)
  - Got `textacy` versions 0.9.1 and 0.10.0 up on `conda-forge` (Issue #294)
  - Added spectral seriation as a term-ordering technique when making a "Termite" visualization by taking advantage of `pandas.DataFrame` functionality, and otherwise tidied up the default for nice-looking plots (PR #295)

#### Fixed:

- Corrected an incorrect and misleading reference in the quickstart docs (Issue #300, PR #302)
- Fixed a bug in the `delete_words()` augmentation transform (Issue #308)

#### Contributors:

Special thanks to @tbsexton, @marius-mather, and @rmax for their contributions! 💐


### 0.10.0 (2020-03-01)

#### New:

- Added a logo to textacy's documentation and social preview :page_with_curl:
- Added type hints throughout the code base, for more expressive type indicators in docstrings and for static type checkers used by developers to code more effectively (PR #289)
- Added a preprocessing function to normalize sequences of repeating characters (Issue #275)

#### Changed:

- Improved core `Corpus` functionality using recent additions to spacy (PR #285)
  - Re-implemented `Corpus.save()` and `Corpus.load()` using spacy's new `DocBin` class, which resolved a few bugs/issues (Issue #254)
  - Added `n_process` arg to `Corpus.add()` to set the number of parallel processes used when adding many items to a corpus, following spacy's updates to `nlp.pipe()` (Issue #277)
  - Bumped minimum spaCy version from 2.0.12 => 2.2.0, accordingly
- Added handling for zero-width whitespaces into `normalize_whitespace()` function (Issue #278)
- Improved a couple rough spots in package administration:
  - Moved package setup information into a declarative configuration file, in an attempt to keep up with evolving best practices for Python packaging
  - Simplified the configuration and interoperability of sphinx + github pages for generating package documentation

#### Fixed:

- Fixed typo in ConceptNet docstring (Issue #280)
- Trained and distributed a `LangIdentifier` model using `scikit-learn==0.22`, to prevent ambiguous errors when trying to load a file that didn't exist (Issues #291, #292)


### 0.9.1 (2019-09-03)

#### Changed:

- Tweaked `TopicModel` class to work with newer versions of `scikit-learn`, and updated version requirements accordingly from `>=0.18.0,<0.21.0` to `>=0.19`

#### Fixed:

- Fixed residual bugs in the script for training language identification pipelines, then trained and released one using `scikit-learn==0.19` to prevent errors for users on that version


### 0.9.0 (2019-09-03)

Note: `textacy` is now PY3-only! 🎉 Specifically, support for PY2.7 has been dropped, and the minimum PY3 version has been bumped to 3.6 (PR #261). See below for related changes.

#### New:

- **Added `augmentation` subpackage for basic text data augmentation** (PR #268, #269)
  - implemented several transformer functions for substituting, inserting, swapping, and deleting elements of text at both the word- and character-level
  - implemented an `Augmenter` class for combining multiple transforms and applying them to spaCy `Doc`s in a randomized but configurable manner
  - **Note:** This API is provisional, and subject to change in future releases.
- **Added `resources` subpackage for standardized access to linguistic resources** (PR #265)
  - **DepecheMood++:** high-coverage emotion lexicons for understanding the emotions evoked by a text. Updated from a previous version, and now features better English data and Italian data with expanded, consistent functionality.
    - removed `lexicon_methods.py` module with previous implementation
  - **ConceptNet:** multilingual knowledge base for representing relationships between words, similar to WordNet. Currently supports getting word antonyms, hyponyms, meronyms, and synonyms in dozens of languages.
- **Added `UDHR` dataset, a collection of translations of the Universal Declaration of Human Rights** (PR #271)

#### Changed:

- Updated and extended functionality previously blocked by PY2 compatibility while reducing code bloat / complexity
  - made many args keyword-only, to prevent user error
  - args accepting strings for directory / file paths now also accept `pathlib.Path` objects, with `pathlib` adopted widely under the hood
  - increased minimum versions and/or uncapped maximum versions of several dependencies, including `jellyfish`, `networkx`, and `numpy`
- Added a Portuguese-specific formulation of Flesch Reading Ease score to `text_stats` (PR #263)
- Reorganized and grouped together some like functionality
  - moved core functionality for loading spaCy langs and making spaCy docs into `spacier.core`, out of `cache.py` and `doc.py`
  - moved some general-purpose functionality from `dataset.utils` to `io.utils` and `utils.py`
  - moved function for loading "hyphenator" out of `cache.py` and into `text_stats.py`, where it's used
- Re-trained and released language identification pipelines using a better mix of training data, for slightly improved performance; also added the script used to train the pipeline
- Changed API Reference docs to show items in source code rather than alphabetical order, which should make the ordering more human-friendly
- Updated repo README and PyPi metadata to be more consistent and representative of current functionality
- Removed previously deprecated `textacy.io.split_record_fields()` function

#### Fixed:

- Fixed a regex for cleaning up crufty terms to prevent catastrophic backtracking in certain edge cases (true story: this bug was encountered in _production code_, and ruined my day)
- Fixed bad handling of edge cases in sCAKE keyterm extraction (Issue #270)
- Changed order in which URL regexes are applied in `preprocessing.replace_urls()` to properly handle certain edge case URLs (Issue #267)

#### Contributors:

Thanks much to @hugoabonizio for the contribution. 🤝


### 0.8.0 (2019-07-14)

#### New and Changed:

- **Refactored and expanded text preprocessing functionality** (PR #253)
  - Moved code from a top-level `preprocess` module into a `preprocessing` sub-package, and reorganized it in the process
  - Added new functions:
    - `replace_hashtags()` to replace hashtags like `#FollowFriday` or `#spacyIRL2019` with `_TAG_`
    - `replace_user_handles()` to replace user handles like `@bjdewilde` or `@spacy_io` with `_USER_`
    - `replace_emojis()` to replace emoji symbols like 😉 or 🚀 with `_EMOJI_`
    - `normalize_hyphenated_words()` to join hyphenated words back together, like `antici-  pation` => `anticipation`
    - `normalize_quotation_marks()` to replace "fancy" quotation marks with simple ascii equivalents, like `“the god particle”` => `"the god particle"`
  - Changed a couple functions for clarity and consistency:
    - `replace_currency_symbols()` now replaces _all_ dedicated ascii and unicode currency symbols with `_CUR_`, rather than just a subset thereof, and no longer provides for replacement with the corresponding currency code (like `€` => `EUR`)
    - `remove_punct()` now has a `fast (bool)` kwarg rather than `method (str)`
  - Removed `normalize_contractions()`, `preprocess_text()`, and `fix_bad_unicode()` functions, since they were bad/awkward and more trouble than they were worth
- **Refactored and expanded keyterm extraction functionality** (PR #257)
  - Moved code from a top-level `keyterms` module into a `ke` sub-package, and cleaned it up / standardized arg names / better shared functionality in the process
  - Added new unsupervised keyterm extraction algorithms: YAKE (`ke.yake()`), sCAKE (`ke.scake()`), and PositionRank (`ke.textrank()`, with non-default parameter values)
  - Added new methods for selecting candidate keyterms: longest matching subsequence candidates (`ke.utils.get_longest_subsequence_candidates()`) and pattern-matching candidates (`ke.utils.get_pattern_matching_candidates()`)
  - Improved speed of SGRank implementation, and generally optimized much of the code
- **Improved document similarity functionality** (PR #256)
  - Added a character ngram-based similarity measure (`similarity.character_ngrams()`), for something that's useful in different contexts than the other measures
  - Removed Jaro-Winkler string similarity measure (`similarity.jaro_winkler()`), since it didn't add much beyond other measures
  - Improved speed of Token Sort Ratio implementation
  - Replaced `python-levenshtein` dependency with `jellyfish`, for its active development, better documentation, and _actually-compliant_ license
- **Added customizability to certain functionality**
  - Added options to `Doc._.to_bag_of_words()` and `Corpus.word_counts()` for filtering out stop words, punctuation, and/or numbers (PR #249)
  - Allowed for objects that _look like_ `sklearn`-style topic modeling classes to be passed into `tm.TopicModel()` (PR #248)
  - Added options to customize rc params used by `matplotlib` when drawing a "termite" plot in `viz.draw_termite_plot()` (PR #248)
- Removed deprecated functions with direct replacements: `io.utils.get_filenames()` and `spacier.components.merge_entities()`

#### Contributors:

Huge thanks to @kjoshi and @zf109 for the PRs! 🙌


### 0.7.1 (2019-06-25)

#### New:

- Added a default, built-in language identification classifier that's moderately fast, moderately accurate, and covers a relatively large number of languages [PR #247]
  - Implemented a Google CLD3-inspired model in `scikit-learn` and trained it on ~1.5M texts in ~130 different languages spanning a wide variety of subject matter and stylistic formality; overall, speed and performance compare favorably to other open-source options (`langid`, `langdetect`, `cld2-cffi`, and `cld3`)
  - Dropped `cld2-cffi` dependency [Issue #246]
- Added `extract.matches()` function to extract spans from a document matching one or more pattern of per-token (attribute, value) pairs, with optional quantity qualifiers; this is a convenient interface to spaCy's rule-based `Matcher` and a more powerful replacement for textacy's existing (now deprecated) `extract.pos_regex_matches()`
- Added `preprocess.normalize_unicode()` function to transform unicode characters into their canonical forms; this is a less-intensive consolation prize for the previously-removed `fix_unicode()` function

#### Changed:

- Enabled loading blank spaCy `Language` pipelines (tokenization only -- no model-based tagging, parsing, etc.) via `load_spacy_lang(name, allow_blank=True)` for use cases that don't rely on annotations; disabled by default to avoid unwelcome surprises
- Changed inclusion/exclusion and de-duplication of entities and ngrams in `to_terms_list()` [Issues #169, #179]
  - `entities = True` => include entities, and drop exact duplicate ngrams
  - `entities = False` => don't include entities, and also drop exact duplicate ngrams
  - `entities = None` => use ngrams as-is without checking against entities
- Moved `to_collection()` function from the `datasets.utils` module to the top-level `utils` module, for use throughout the code base
- Added `quoting` option to `io.read_csv()` and `io.write_csv()`, for problematic cases
- Deprecated the `spacier.components.merge_entities()` pipeline component, an implementation of which has since been added into spaCy itself
- Updated documentation for developer convenience and reader clarity
  - Split API reference docs into related chunks, rather than having them all together in one long page, and tidied up headers
  - Fixed errors / inconsistencies in various docstrings (a never-ending struggle...)
  - Ported package readme and changelog from `.rst` to `.md` format

#### Fixed:

- The `NotImplementedError` previously added to `preprocess.fix_unicode()` is now _raised_ rather than returned [Issue #243]


### 0.7.0 (2019-05-13)

#### New and Changed:

- **Removed textacy.Doc, and split its functionality into two parts**
  - **New:** Added `textacy.make_spacy_doc()` as a convenient and flexible entry point
    for making spaCy `Doc` s from text or (text, metadata) pairs, with optional
    spaCy language pipeline specification. It's similar to `textacy.Doc.__init__`,
    with the exception that text and metadata are passed in together as a 2-tuple.
  - **New:** Added a variety of custom doc property and method extensions to
    the global `spacy.tokens.Doc` class, accessible via its `Doc._` "underscore"
    property. These are similar to the properties/methods on `textacy.Doc`,
    they just require an interstitial underscore. For example,
    `textacy.Doc.to_bag_of_words()` => `spacy.tokens.Doc._.to_bag_of_words()`.
  - **New:** Added functions for setting, getting, and removing these extensions.
    Note that they are set automatically when textacy is imported.
- **Simplified and improved performance of textacy.Corpus**
  - Documents are now added through a simpler API, either in `Corpus.__init__`
    or `Corpus.add()`; they may be one or a stream of texts, (text, metadata)
    pairs, or existing spaCy `Doc` s. When adding many documents, the spaCy
    language processing pipeline is used in a faster and more efficient way.
  - Saving / loading corpus data to disk is now more efficient and robust.
  - Note: `Corpus` is now a collection of spaCy `Doc` s rather than `textacy.Doc` s.
- **Simplified, standardized, and added Dataset functionality**
  - **New:** Added an `IMDB` dataset, built on the classic 2011 dataset
    commonly used to train sentiment analysis models.
  - **New:** Added a base `Wikimedia` dataset, from which a reworked
    `Wikipedia` dataset and a separate `Wikinews` dataset inherit.
    The underlying data source has changed, from XML db dumps of raw wiki markup
    to JSON db dumps of (relatively) clean text and metadata; now, the code is
    simpler, faster, and totally language-agnostic.
  - `Dataset.records()` now streams (text, metadata) pairs rather than a dict
    containing both text and metadata, so users don't need to know field names
    and split them into separate streams before creating `Doc` or `Corpus`
    objects from the data.
  - Filtering and limiting the number of texts/records produced is now clearer
    and more consistent between `.texts()` and `.records()` methods on
    a given `Dataset` --- and more performant!
  - Downloading datasets now always shows progress bars and saves to the same
    file names. When appropriate, downloaded archive files' contents are
    automatically extracted for easy inspection.
  - Common functionality (such as validating filter values) is now standardized
    and consolidated in the `datasets.utils` module.
- **Quality of life improvements**
  - Reduced load time for `import textacy` from ~2-3 seconds to ~1 second,
    by lazy-loading expensive variables, deferring a couple heavy imports, and
    dropping a couple dependencies. Specifically:
    - `ftfy` was dropped, and a `NotImplementedError` is now raised
      in textacy's wrapper function, `textacy.preprocess.fix_bad_unicode()`.
      Users with bad unicode should now directly call `ftfy.fix_text()`.
    - `ijson` was dropped, and the behavior of `textacy.read_json()`
      is now simpler and consistent with other functions for line-delimited data.
    - `mwparserfromhell` was dropped, since the reworked `Wikipedia` dataset
      no longer requires complicated and slow parsing of wiki markup.
  - Renamed certain functions and variables for clarity, and for consistency with
    existing conventions:
    - `textacy.load_spacy()` => `textacy.load_spacy_lang()`
    - `textacy.extract.named_entities()` => `textacy.extract.entities()`
    - `textacy.data_dir` => `textacy.DEFAULT_DATA_DIR`
    - `filename` => `filepath` and `dirname` => `dirpath` when specifying
      full paths to files/dirs on disk, and `textacy.io.utils.get_filenames()`
      => `textacy.io.utils.get_filepaths()` accordingly
    - compiled regular expressions now consistently start with `RE_`
    - `SpacyDoc` => `Doc`, `SpacySpan` => `Span`, `SpacyToken` => `Token`,
      `SpacyLang` => `Language` as variables and in docs
  - Removed deprecated functionality
    - top-level `spacy_utils.py` and `spacy_pipelines.py` are gone;
      use equivalent functionality in the `spacier` subpackage instead
    - `math_utils.py` is gone; it was long neglected, and never actually used
  - Replaced `textacy.compat.bytes_to_unicode()` and `textacy.compat.unicode_to_bytes()`
    with `textacy.compat.to_unicode()` and `textacy.compat.to_bytes()`, which
    are safer and accept either binary or text strings as input.
  - Moved and renamed language detection functionality,
    `textacy.text_utils.detect_language()` => `textacy.lang_utils.detect_lang()`.
    The idea is to add more/better lang-related functionality here in the future.
  - Updated and cleaned up documentation throughout the code base.
  - Added and refactored _many_ tests, for both new and old functionality,
    significantly increasing test coverage while significantly reducing run-time.
    Also, added a proper coverage report to CI builds. This should help prevent
    future errors and inspire better test-writing.
  - Bumped the minimum required spaCy version: `v2.0.0` => `v2.0.12`,
    for access to their full set of custom extension functionality.

#### Fixed:

- The progress bar during an HTTP download now always closes, preventing weird
  nesting issues if another bar is subsequently displayed.
- Filtering datasets by multiple values performed either a logical AND or OR
  over the values, which was confusing; now, a logical OR is always performed.
- The existence of files/directories on disk is now checked _properly_ via
  `os.path.isfile()` or `os.path.isdir()`, rather than `os.path.exists()`.
- Fixed a variety of formatting errors raised by sphinx when generating HTML docs.


### 0.6.3 (2019-03-23)

#### New:

- Added a proper contributing guide and code of conduct, as well as separate
  GitHub issue templates for different user situations. This should help folks
  contribute to the project more effectively, and make maintaining it a bit easier,
  too. [Issue #212]
- Gave the documentation a new look, using a template popularized by `requests`.
  Added documentation on dealing with multi-lingual datasets. [Issue #233]
- Made some minor adjustments to package dependencies, the way they're specified,
  and the Travis CI setup, making for a faster and better development experience.
- Confirmed and enabled compatibility with v2.1+ of `spacy`. :dizzy:

#### Changed:

- Improved the `Wikipedia` dataset class in a variety of ways: it can now read
  Wikinews db dumps; access records in namespaces other than the usual "0"
  (such as category pages in namespace "14"); parse and extract category pages
  in several languages, including in the case of bad wiki markup; and filter out
  section headings from the accompanying text via an `include_headings` kwarg.
  [PR #219, #220, #223, #224, #231]
- Removed the `transliterate_unicode()` preprocessing function that transliterated
  non-ascii text into a reasonable ascii approximation, for technical and
  philosophical reasons. Also removed its GPL-licensed `unidecode` dependency,
  for legal-ish reasons. [Issue #203]
- Added convention-abiding `exclude` argument to the function that writes
  `spacy` docs to disk, to limit which pipeline annotations are serialized.
  Replaced the existing but non-standard `include_tensor` arg.
- Deprecated the `n_threads` argument in `Corpus.add_texts()`, which had not
  been working in `spacy.pipe` for some time and, as of v2.1, is defunct.
- Made many tests model- and python-version agnostic and thus less likely to break
  when `spacy` releases new and improved models.
- Auto-formatted the entire code base using `black`; the results aren't always
  more readable, but they are pleasingly consistent.

#### Fixed:

- Fixed bad behavior of `key_terms_from_semantic_network()`, where an error
  would be raised if no suitable key terms could be found; now, an empty list
  is returned instead. [Issue #211]
- Fixed variable name typo so `GroupVectorizer.fit()` actually works. [Issue #215]
- Fixed a minor typo in the quick-start docs. [PR #217]
- Check for and filter out any named entities that are entirely whitespace,
  seemingly caused by an issue in `spacy`.
- Fixed an undefined variable error when merging spans. [Issue #225]
- Fixed a unicode/bytes issue in experimental function for deserializing `spacy`
  docs in "binary" format. [Issue #228, PR #229]

#### Contributors:

Many thanks to @abevieiramota, @ckot, @Jude188, and @digest0r for their help!


### 0.6.2 (2018-07-19)

#### Changed:

- Add a `spacier.util` module, and add / reorganize relevant functionality
  - move (most) `spacy_util` functions here, and add a deprecation warning to
    the `spacy_util` module
  - rename `normalized_str()` => `get_normalized_text()`, for consistency and clarity
  - add a function to split long texts up into chunks but combine them into
    a single `Doc`. This is a workaround for a current limitation of spaCy's
    neural models, whose RAM usage scales with the length of input text.
- Add experimental support for reading and writing spaCy docs in binary format,
  where multiple docs are contained in a single file. This functionality was
  supported by spaCy v1, but is not in spaCy v2; I've implemented a workaround
  that should work well in most situations, but YMMV.
- Package documentation is now "officially" hosted on GitHub pages. The docs
  are automatically built on and deployed from Travis via `doctr`, so they
  stay up-to-date with the master branch on GitHub. Maybe someday I'll get
  ReadTheDocs to successfully build `textacy` once again...
- Minor improvements/updates to documentation

#### Fixed:

- Add missing return statement in deprecated `text_stats.flesch_readability_ease()`
  function (Issue #191)
- Catch an empty graph error in bestcoverage-style keyterm ranking (Issue #196)
- Fix mishandling when specifying a single named entity type to in/exclude in
  `extract.named_entities` (Issue #202)
- Make `networkx` usage in keyterms module compatible with v1.11+ (Issue #199)


### 0.6.1 (2018-04-11)

#### New:

- **Add a new spacier sub-package for spaCy-oriented functionality** (#168, #187)
  - Thus far, this includes a `components` module with two custom spaCy
    pipeline components: one to compute text stats on parsed documents, and
    another to merge named entities into single tokens in an efficient manner.
    More to come!
  - Similar functionality in the top-level `spacy_pipelines` module has been
    deprecated; it will be removed in v0.7.0.

#### Changed:

- Update the readme, usage, and API reference docs to be clearer and (I hope)
  more useful. (#186)
- Removing punctuation from a text via the `preprocessing` module now replaces
  punctuation marks with a single space rather than an empty string. This gives
  better behavior in many situations; for example, "won't" => "won t" rather than
  "wont", the latter of which is a valid word with a different meaning.
- Categories are now correctly extracted from non-English language Wikipedia
  datasets, starting with French and German and extendable to others. (#175)
- Log progress when adding documents to a corpus. At the debug level, every
  doc's addition is logged; at the info level, only one message per batch
  of documents is logged. (#183)

#### Fixed:

- Fix two breaking typos in `extract.direct_quotations()`. (issue #177)
- Prevent crashes when adding non-parsed documents to a `Corpus`. (#180)
- Fix bugs in `keyterms.most_discriminating_terms()` that used `vsm`
  functionality as it was *before* the changes in v0.6.0. (#189)
- Fix a breaking typo in `vsm.matrix_utils.apply_idf_weighting()`, and rename
  the problematic kwarg for consistency with related functions. (#190)

#### Contributors:

Big thanks to @sammous, @dixiekong (nice name!), and @SandyRogers for the pull
requests, and many more for pointing out various bugs and the rougher edges /
unsupported use cases of this package.


### 0.6.0 (2018-02-25)

#### Changed:

- **Rename, refactor, and extend I/O functionality** (PR #151)
  - Related read/write functions were moved from `read.py` and `write.py` into
    format-specific modules, and similar functions were consolidated into one
    with the addition of an arg. For example, `write.write_json()` and
    `write.write_json_lines()` => `json.write_json(lines=True|False)`.
  - Useful functionality was added to a few readers/writers. For example,
    `write_json()` now automatically handles python dates/datetimes, writing
    them to disk as ISO-formatted strings rather than raising a TypeError
    ("datetime is not JSON serializable", ugh). CSVs can now be written to /
    read from disk when each row is a dict rather than a list. Reading/writing
    HTTP streams now allows for basic authentication.
  - Several things were renamed to improve clarity and consistency from a user's
    perspective, most notably the subpackage name: `fileio` => `io`. Others:
    `read_file()` and `write_file()` => `read_text()` and `write_text()`;
    `split_record_fields()` => `split_records()`, although I kept an alias
    to the old function for folks; `auto_make_dirs` boolean kwarg => `make_dirs`.
  - `io.open_sesame()` now handles zip files (provided they contain only 1 file)
    as it already does for gzip, bz2, and lzma files. On a related note, Python 2
    users can now open lzma (`.xz`) files if they've installed `backports.lzma`.
- **Improve, refactor, and extend vector space model functionality** (PRs #156 and #167)
  - BM25 term weighting and document-length normalization were implemented, and
    and users can now flexibly add and customize individual components of an
    overall weighting scheme (local scaling + global scaling + doc-wise normalization).
    For API sanity, several additions and changes to the `Vectorizer` init
    params were required --- sorry bout it!
  - Given all the new weighting possibilities, a `Vectorizer.weighting` attribute
    was added for curious users, to give a mathematical representation of how
    values in a doc-term matrix are being calculated. Here's a simple and a
    not-so-simple case:

    ```python
    >>> Vectorizer(apply_idf=True, idf_type='smooth').weighting
    'tf * log((n_docs + 1) / (df + 1)) + 1'
    >>> Vectorizer(tf_type='bm25', apply_idf=True, idf_type='smooth', apply_dl=True).weighting
    '(tf * (k + 1)) / (tf + k * (1 - b + b * (length / avg(lengths))) * log((n_docs - df + 0.5) / (df + 0.5))'
    ```

  - Terms are now sorted alphabetically after fitting, so you'll have a consistent
    and interpretable ordering in your vocabulary and doc-term-matrix.
  - A `GroupVectorizer` class was added, as a child of `Vectorizer` and
    an extension of typical document-term matrix vectorization, in which each
    row vector corresponds to the weighted terms co-occurring in a single document.
    This allows for customized grouping, such as by a shared author or publication year,
    that may span multiple documents, without forcing users to merge /concatenate
    those documents themselves.
  - Lastly, the `vsm.py` module was refactored into a `vsm` subpackage with
    two modules. Imports should stay the same, but the code structure is now
    more amenable to future additions.
- **Miscellaneous additions and improvements**
  - Flesch Reading Ease in the `textstats` module is now multi-lingual! Language-
    specific formulations for German, Spanish, French, Italian, Dutch, and Russian
    were added, in addition to (the default) English. (PR #158, prompted by Issue #155)
  - Runtime performance, as well as docs and error messages, of functions for
    generating semantic networks from lists of terms or sentences were improved. (PR #163)
  - Labels on named entities from which determiners have been dropped are now
    preserved. There's still a minor gotcha, but it's explained in the docs.
  - The size of `textacy`'s data cache can now be set via an environment
    variable, `TEXTACY_MAX_CACHE_SIZE`, in case the default 2GB cache doesn't
    meet your needs.
  - Docstrings were improved in many ways, large and small, throughout the code.
    May they guide you even more effectively than before!
  - The package version is now set from a single source. This isn't for you so
    much as me, but it does prevent confusing version mismatches b/w code, pypi,
    and docs.
  - All tests have been converted from `unittest` to `pytest` style. They
    run faster, they're more informative in failure, and they're easier to extend.

#### Fixed:

- Fixed an issue where existing metadata associated with a spacy Doc was being
  overwritten with an empty dict when using it to initialize a textacy Doc.
  Users can still overwrite existing metadata, but only if they pass in new data.
- Added a missing import to the README's usage example. (#149)
- The intersphinx mapping to `numpy` got fixed (and items for `scipy` and
  `matplotlib` were added, too). Taking advantage of that, a bunch of broken
  object links scattered throughout the docs got fixed.
- Fixed broken formatting of old entries in the changelog, for your reading pleasure.


### 0.5.0 (2017-12-04)

#### Changed:

- **Bumped version requirement for spaCy from < 2.0 to >= 2.0** --- textacy no longer
  works with spaCy 1.x! It's worth the upgrade, though. v2.0's new features and
  API enabled (or required) a few changes on textacy's end
  - `textacy.load_spacy()` takes the same inputs as the new `spacy.load()`,
    i.e. a package `name` string and an optional list of pipes to `disable`
  - textacy's `Doc` metadata and language string are now stored in `user_data`
    directly on the spaCy `Doc` object; although the API from a user's perspective
    is unchanged, this made the next change possible
  - `Doc` and `Corpus` classes are now de/serialized via pickle into a single
    file --- no more side-car JSON files for metadata! Accordingly, the `.save()`
    and `.load()` methods on both classes have a simpler API: they take
    a single string specifying the file on disk where data is stored.
- **Cleaned up docs, imports, and tests throughout the entire code base.**
  - docstrings and https://textacy.readthedocs.io 's API reference are easier to
    read, with better cross-referencing and far fewer broken web links
  - namespaces are less cluttered, and textacy's source code is easier to follow
  - `import textacy` takes less than half the time from before
  - the full test suite also runs about twice as fast, and most tests are now
    more robust to changes in the performance of spaCy's models
  - consistent adherence to conventions eases users' cognitive load :)
- **The module responsible for caching loaded data in memory was cleaned up and
  improved**, as well as renamed: from `data.py` to `cache.py`, which is more
  descriptive of its purpose. Otherwise, you shouldn't notice much of a difference
  besides *things working correctly*.
  - All loaded data (e.g. spacy language pipelines) is now cached together in a
    single LRU cache whose max size is set to 2GB, and the size of each element
    in the cache is now accurately computed. (tl;dr: `sys.getsizeof` does not
    work on non-built-in objects like, say, a `spacy.tokens.Doc`.)
  - Loading and downloading of the DepecheMood resource is now less hacky and
    weird, and much closer to how users already deal with textacy's various
    `Dataset` s, In fact, it can be downloaded in exactly the same way as the
    datasets via textacy's new CLI: `$ python -m textacy download depechemood`.
    P.S. A brief guide for using the CLI got added to the README.
- **Several function/method arguments marked for deprecation have been removed.**
  If you've been ignoring the warnings that print out when you use `lemmatize=True`
  instead of `normalize='lemma'` (etc.), now is the time to update your calls!
  - Of particular note: The `readability_stats()` function has been removed;
    use `TextStats(doc).readability_stats` instead.

#### Fixed:

- In certain situations, the text of a spaCy span was being returned without
  whitespace between tokens; that has been avoided in textacy, and the source bug
  in spaCy got fixed (by yours truly! https://github.com/explosion/spaCy/pull/1621).
- When adding already-parsed `Doc`s to a `Corpus`, including `metadata`
  now correctly overwrites any existing metadata on those docs.
- Fixed a couple related issues involving the assignment of a 2-letter language
  string to the `.lang` attribute of `Doc` and `Corpus` objects.
- textacy's CLI wasn't correctly handling certain dataset kwargs in all cases;
  now, all kwargs get to their intended destinations.


### 0.4.2 (2017-11-28)

#### New:

- Added a CLI for downloading `textacy`-related data, inspired by the `spaCy`
  equivalent. It's *temporarily* undocumented, but to see available commands and
  options, just pass the usual flag: `$ python -m textacy --help`. Expect more
  functionality (and docs!) to be added soonish. (#144)
  - Note: The existing `Dataset.download()` methods work as before, and in fact,
    they are being called under the hood from the command line.

#### Changed:

- Made usage of `networkx` v2.0-compatible, and therefore dropped the <2.0
  version requirement on that dependency. Upgrade as you please! (#131)
- Improved the regex for identifying phone numbers so that it's easier to view
  and interpret its matches. (#128)

#### Fixed:

- Fixed caching of counts on `textacy.Doc` instance-specific, rather than
  shared by all instances of the class. Oops.
- Fixed currency symbols regex, so as not to replace all instances of the letter "z"
  when a custom string is passed into `replace_currency_symbols()`. (#137)
- Fixed README usage example, which skipped downloading of dataset data. Btw,
  see above for another way! (#124)
- Fixed typo in the API reference, which included the SupremeCourt dataset twice
  and omitted the RedditComments dataset. (#129)
- Fixed typo in `RedditComments.download()` that prevented it from downloading
  any data. (#143)

#### Contributors:

Many thanks to @asifm, @harryhoch, and @mdlynch37 for submitting PRs!


### 0.4.1 (2017-07-27)

#### Changed:

- Added key classes to the top-level `textacy` imports, for convenience:
  - `textacy.text_stats.TextStats` => `textacy.TextStats`
  - `textacy.vsm.Vectorizer` => `textacy.Vectorizer`
  - `textacy.tm.TopicModel` => `textacy.TopicModel`
- Added tests for `textacy.Doc` and updated the README's usage example

#### Fixed:

- Added explicit encoding when opening Wikipedia database files in text mode to
  resolve an issue when doing so without encoding on Windows (PR #118)
- Fixed `keyterms.most_discriminating_terms` to use the `vsm.Vectorizer` class
  rather than the `vsm.doc_term_matrix` function that it replaced (PR #120)
- Fixed mishandling of a couple optional args in `Doc.to_terms_list`

#### Contributors:

Thanks to @minketeer and @Gregory-Howard for the fixes!


### 0.4.0 (2017-06-21)

#### New and Changed:

- Refactored and expanded built-in `corpora`, now called `datasets` (PR #112)
  - The various classes in the old `corpora` subpackage had a similar but
    frustratingly not-identical API. Also, some fetched the corresponding dataset
    automatically, while others required users to do it themselves. Ugh.
  - These classes have been ported over to a new `datasets` subpackage; they
    now have a consistent API, consistent features, and consistent documentation.
    They also have some new functionality, including pain-free downloading of
    the data and saving it to disk in a stream (so as not to use all your RAM).
  - Also, there's a new dataset: A collection of 2.7k Creative Commons texts
    from the Oxford Text Archive, which rounds out the included datasets with
    English-language, 16th-20th century _literary_ works. (h/t @JonathanReeve)
- A `Vectorizer` class to convert tokenized texts into variously weighted
  document-term matrices (Issue #69, PR #113)
  - This class uses the familiar `scikit-learn` API (which is also consistent
    with the `textacy.tm.TopicModel` class) to convert one or more documents
    in the form of "term lists" into weighted vectors. An initial set of documents
    is used to build up the matrix vocabulary (via `.fit()`), which can then
    be applied to new documents (via `.transform()`).
  - It's similar in concept and usage to sklearn's `CountVectorizer` or
    `TfidfVectorizer`, but doesn't convolve the tokenization task as they do.
    This means users have more flexibility in deciding which terms to vectorize.
    This class outright replaces the `textacy.vsm.doc_term_matrix()` function.
- Customizable automatic language detection for `Doc` s
  - Although `cld2-cffi` is fast and accurate, its installation is problematic
    for some users. Since other language detection libraries are available
    (e.g. [`langdetect`](https://github.com/Mimino666/langdetect) and
    [`langid`](https://github.com/saffsd/langid.py)), it makes sense to let
    users choose, as needed or desired.
  - First, `cld2-cffi` is now an optional dependency, i.e. is not installed
    by default. To install it, do `pip install textacy[lang]` or (for it and
    all other optional deps) do `pip install textacy[all]`. (PR #86)
  - Second, the `lang` param used to instantiate `Doc` objects may now
    be a callable that accepts a unicode string and returns a standard 2-letter
    language code. This could be a function that uses `langdetect` under the
    hood, or a function that always returns "de" -- it's up to users. Note that
    the default value is now `textacy.text_utils.detect_language()`, which
    uses `cld2-cffi`, so the default behavior is unchanged.
- Customizable punctuation removal in the `preprocessing` module (Issue #91)
  - Users can now specify which punctuation marks they wish to remove, rather
    than always removing _all_ marks.
  - In the case that all marks are removed, however, performance is now 5-10x
    faster by using Python's built-in `str.translate()` method instead of
    a regular expression.
- `textacy`, installable via `conda` (PR #100)
  - The package has been added to Conda-Forge ([here](https://github.com/conda-forge/textacy-feedstock)),
    and installation instructions have been added to the docs. Hurray!
- `textacy`, now with helpful badges
  - Builds are now automatically tested via Travis CI, and there's a badge in
    the docs showing whether the build passed or not. The days of my ignoring
    broken tests in `master` are (probably) over...
  - There are also badges showing the latest releases on GitHub, pypi, and
    conda-forge (see above).

#### Fixed:

- Fixed the check for overlap between named entities and unigrams in the
  `Doc.to_terms_list()` method (PR #111)
- `Corpus.add_texts()` uses CPU_COUNT - 1 threads by default, rather than
  always assuming that 4 cores are available (Issue #89)
- Added a missing coding declaration to a test file, without which tests failed
  for Python 2 (PR #99)
- `readability_stats()` now catches an exception raised on empty documents and
  logs a message, rather than barfing with an unhelpful `ZeroDivisionError`.
  (Issue #88)
- Added a check for empty terms list in `terms_to_semantic_network` (Issue #105)
- Added and standardized module-specific loggers throughout the code base; not
  a bug per sé, but certainly some much-needed housecleaning
- Added a note to the docs about expectations for bytes vs. unicode text (PR #103)

#### Contributors:

Thanks to @henridwyer, @rolando, @pavlin99th, and @kyocum for their contributions!
:raised_hands:


### 0.3.4 (2017-04-17)

#### New and Changed:

- Improved and expanded calculation of basic counts and readability statistics
  in `text_stats` module.
  - Added a `TextStats()` class for more convenient, granular access to
    individual values. See usage docs for more info. When calculating, say, just
    one readability statistic, performance with this class should be slightly better;
    if calculating _all_ statistics, performance is worse owing to unavoidable,
    added overhead in Python for variable lookups. The legacy function
    `text_stats.readability_stats()` still exists and behaves as before, but a
    deprecation warning is displayed.
  - Added functions for calculating Wiener Sachtextformel (PR #77), LIX, and GULPease
    readability statistics.
  - Added number of long words and number of monosyllabic words to basic counts.
- Clarified the need for having spacy models installed for most use cases of textacy,
  in addition to just the spacy package.
  - README updated with comments on this, including links to more extensive spacy
    documentation. (Issues #66 and #68)
  - Added a function, `compat.get_config()` that includes information about which
    (if any) spacy models are installed.
  - Recent changes to spacy, including a warning message, will also make model
    problems more apparent.
- Added an `ngrams` parameter to `keyterms.sgrank()`, allowing for more flexibility
  in specifying valid keyterm candidates for the algorithm. (PR #75)
- Dropped dependency on `fuzzywuzzy` package, replacing usage of
  `fuzz.token_sort_ratio()`
  with a textacy equivalent in order to avoid license incompatibilities. As a bonus,
  the new code seems to perform faster! (Issue #62)
  - Note: Outputs are now floats in [0.0, 1.0], consistent with other similarity
    functions, whereas before outputs were ints in [0, 100]. This has implications
    for `match_threshold` values passed to `similarity.jaccard()`; a warning
    is displayed and the conversion is performed automatically, for now.
- A MANIFEST.in file was added to include docs, tests, and distribution files in the source distribution. This is just good practice. (PR #65)

#### Fixed:

- Known acronym-definition pairs are now properly handled in
  `extract.acronyms_and_definitions()` (Issue #61)
- WikiReader no longer crashes on null page element content while parsing (PR #64)
- Fixed a rare but perfectly legal edge case exception in `keyterms.sgrank()`,
  and added a window width sanity check. (Issue #72)
- Fixed assignment of 2-letter language codes to `Doc` and `Corpus` objects
  when the lang parameter is specified as a full spacy model name.
- Replaced several leftover print statements with proper logging functions.

#### Contributors:

Big thanks to @oroszgy, @rolando, @covuworie, and @RolandColored for the pull requests!


### 0.3.3 (2017-02-10)

#### New and Changed:

- Added a consistent `normalize` param to functions and methods that require
  token/span text normalization. Typically, it takes one of the following values:
  'lemma' to lemmatize tokens, 'lower' to lowercase tokens, False-y to *not* normalize
  tokens, or a function that converts a spacy token or span into a string, in
  whatever way the user prefers (e.g. `spacy_utils.normalized_str()`).
  - Functions modified to use this param:
    `Doc.to_bag_of_terms()`,
    `Doc.to_bag_of_words()`,
    `Doc.to_terms_list()`,
    `Doc.to_semantic_network()`,
    `Corpus.word_freqs()`,
    `Corpus.word_doc_freqs()`,
    `keyterms.sgrank()`,
    `keyterms.textrank()`,
    `keyterms.singlerank()`,
    `keyterms.key_terms_from_semantic_network()`,
    `network.terms_to_semantic_network()`,
    `network.sents_to_semantic_network()`
- Tweaked `keyterms.sgrank()` for higher quality results and improved internal
  performance.
- When getting both n-grams and named entities with `Doc.to_terms_list()`, filtering
  out numeric spans for only one is automatically extended to the other. This prevents
  unexpected behavior, such as passing `filter_nums=True` but getting numeric named
  entities back in the terms list.

#### Fixed:

- `keyterms.sgrank()` no longer crashes if a term is missing from `idfs` mapping.
  (@jeremybmerrill, issue #53)
- Proper nouns are no longer excluded from consideration as keyterms in `keyterms.sgrank()`
  and `keyterms.textrank()`. (@jeremybmerrill, issue #53)
- Empty strings are now excluded from consideration as keyterms — a bug inherited
  from spaCy. (@mlehl88, issue #58)


### 0.3.2 (2016-11-15)

#### New and Changed:

- Preliminary inclusion of custom spaCy pipelines
  - updated `load_spacy()` to include explicit path and create_pipeline kwargs,
    and removed the already-deprecated `load_spacy_pipeline()` function to avoid
    confusion around spaCy languages and pipelines
  - added `spacy_pipelines` module to hold implementations of custom spaCy pipelines,
    including a basic one that merges entities into single tokens
  - note: necessarily bumped minimum spaCy version to 1.1.0+
  - see the announcement here: https://explosion.ai/blog/spacy-deep-learning-keras
- To reduce code bloat, made the `matplotlib` dependency optional and dropped
  the `gensim` dependency
  - to install `matplotlib` at the same time as textacy, do `$ pip install textacy[viz]`
  - bonus: `backports.csv` is now only installed for Py2 users
  - thanks to @mbatchkarov for the request
- Improved performance of `textacy.corpora.WikiReader().texts()`; results should
  stream faster and have cleaner plaintext content than when they were produced
  by `gensim`. This *should* also fix a bug reported in Issue #51 by @baisk
- Added a `Corpus.vectors` property that returns a matrix of shape
  (# documents, vector dim) containing the average word2vec-style vector
  representation of constituent tokens for all `Doc` s


### 0.3.1 (2016-10-19)

#### Changed:

- Updated spaCy dependency to the latest v1.0.1; set a floor on other dependencies'
  versions to make sure everyone's running reasonably up-to-date code

#### Fixed:

- Fixed incorrect kwarg in `sgrank` 's call to `extract.ngrams()` (@patcollis34, issue #44)
- Fixed import for `cachetool` 's `hashkey`, which changed in the v2.0 (@gramonov, issue #45)


### 0.3.0 (2016-08-23)

#### New and Changed:

- Refactored and streamlined `TextDoc`; changed name to `Doc`
  - simplified init params: `lang` can now be a language code string or an equivalent
    `spacy.Language` object, and `content` is either a string or `spacy.Doc`;
    param values and their interactions are better checked for errors and inconsistencies
  - renamed and improved methods transforming the Doc; for example, `.as_bag_of_terms()`
    is now `.to_bag_of_terms()`, and terms can be returned as integer ids (default)
    or as strings with absolute, relative, or binary frequencies as weights
  - added performant `.to_bag_of_words()` method, at the cost of less customizability
    of what gets included in the bag (no stopwords or punctuation); words can be
    returned as integer ids (default) or as strings with absolute, relative, or
    binary frequencies as weights
  - removed methods wrapping `extract` functions, in favor of simply calling that
    function on the Doc (see below for updates to `extract` functions to make
    this more convenient); for example, `TextDoc.words()` is now `extract.words(Doc)`
  - removed `.term_counts()` method, which was redundant with `Doc.to_bag_of_terms()`
  - renamed `.term_count()` => `.count()`, and checking + caching results is now
    smarter and faster
- Refactored and streamlined `TextCorpus`; changed name to `Corpus`
  - added init params: can now initialize a `Corpus` with a stream of texts,
    spacy or textacy Docs, and optional metadatas, analogous to `Doc`; accordingly,
    removed `.from_texts()` class method
  - refactored, streamlined, *bug-fixed*, and made consistent the process of
    adding, getting, and removing documents from `Corpus`
    - getting/removing by index is now equivalent to the built-in `list` API:
      `Corpus[:5]` gets the first 5 `Doc`s, and `del Corpus[:5]` removes the
      first 5, automatically keeping track of corpus statistics for total
      \# docs, sents, and tokens
    - getting/removing by boolean function is now done via the `.get()` and `.remove()`
      methods, the latter of which now also correctly tracks corpus stats
    - adding documents is split across the `.add_text()`, `.add_texts()`, and
      `.add_doc()` methods for performance and clarity reasons
  - added `.word_freqs()` and `.word_doc_freqs()` methods for getting a mapping
    of word (int id or string) to global weight (absolute, relative, binary, or
    inverse frequency); akin to a vectorized representation (see: `textacy.vsm`)
    but in non-vectorized form, which can be useful
  - removed `.as_doc_term_matrix()` method, which was just wrapping another function;
    so, instead of `corpus.as_doc_term_matrix((doc.as_terms_list() for doc in corpus))`,
    do `textacy.vsm.doc_term_matrix((doc.to_terms_list(as_strings=True) for doc in corpus))`
- Updated several `extract` functions
  - almost all now accept either a `textacy.Doc` or `spacy.Doc` as input
  - renamed and improved parameters for filtering for or against certain POS or NE
    types; for example, `good_pos_tags` is now `include_pos`, and will accept
    either a single POS tag as a string or a set of POS tags to filter for; same
    goes for `exclude_pos`, and analogously `include_types`, and `exclude_types`
- Updated corpora classes for consistency and added flexibility
  - enforced a consistent API: `.texts()` for a stream of plain text documents
    and `.records()` for a stream of dicts containing both text and metadata
  - added filtering options for `RedditReader`, e.g. by date or subreddit,
    consistent with other corpora (similar tweaks to `WikiReader` may come later,
    but it's slightly more complicated...)
  - added a nicer `repr` for `RedditReader` and `WikiReader` corpora, consistent
    with other corpora
- Moved `vsm.py` and `network.py` into the top-level of `textacy` and thus
  removed the `representations` subpackage
  - renamed `vsm.build_doc_term_matrix()` => `vsm.doc_term_matrix()`, because
    the "build" part of it is obvious
- Renamed `distance.py` => `similarity.py`; all returned values are now similarity
  metrics in the interval [0, 1], where higher values indicate higher similarity
- Renamed `regexes_etc.py` => `constants.py`, without additional changes
- Renamed `fileio.utils.split_content_and_metadata()` => `fileio.utils.split_record_fields()`,
  without further changes (except for tweaks to the docstring)
- Added functions to read and write delimited file formats: `fileio.read_csv()`
  and `fileio.write_csv()`, where the delimiter can be any valid one-char string;
  gzip/bzip/lzma compression is handled automatically when available
- Added better and more consistent docstrings and usage examples throughout
  the code base


### 0.2.8 (2016-08-03)

#### New:

- Added two new corpora!
  - the CapitolWords corpus: a collection of 11k speeches (~7M tokens) given by
    the main protagonists of the 2016 U.S. Presidential election that had
    previously served in the U.S. Congress — including Hillary Clinton, Bernie Sanders,
    Barack Obama, Ted Cruz, and John Kasich — from January 1996 through June 2016
  - the SupremeCourt corpus: a collection of 8.4k court cases (~71M tokens)
    decided by the U.S. Supreme Court from 1946 through 2016, with metadata on
    subject matter categories, ideology, and voting patterns
  - **DEPRECATED:** the Bernie and Hillary corpus, which is a small subset of
    CapitolWords that can be easily recreated by filtering CapitolWords by
    `speaker_name={'Bernie Sanders', 'Hillary Clinton'}`

#### Changed:

- Refactored and improved `fileio` subpackage
  - moved shared (read/write) functions into separate `fileio.utils` module
  - almost all read/write functions now use `fileio.utils.open_sesame()`,
    enabling seamless fileio for uncompressed or gzip, bz2, and lzma compressed
    files; relative/user-home-based paths; and missing intermediate directories.
    NOTE: certain file mode / compression pairs simply don't work (this is Python's
    fault), so users may run into exceptions; in Python 3, you'll almost always
    want to use text mode ('wt' or 'rt'), but in Python 2, users can't read or
    write compressed files in text mode, only binary mode ('wb' or 'rb')
  - added options for writing json files (matching stdlib's `json.dump()`) that
    can help save space
  - `fileio.utils.get_filenames()` now matches for/against a regex pattern rather
    than just a contained substring; using the old params will now raise a
    deprecation warning
  - **BREAKING:** `fileio.utils.split_content_and_metadata()` now has `itemwise=False`
    by default, rather than `itemwise=True`, which means that splitting
    multi-document streams of content and metadata into parallel iterators is
    now the default action
  - added `compression` param to `TextCorpus.save()` and `.load()` to optionally
    write metadata json file in compressed form
  - moved `fileio.write_conll()` functionality to `export.doc_to_conll()`, which
    converts a spaCy doc into a ConLL-U formatted string; writing that string to
    disk would require a separate call to `fileio.write_file()`
- Cleaned up deprecated/bad Py2/3 `compat` imports, and added better functionality
  for Py2/3 strings
  - now `compat.unicode_type` used for text data, `compat.bytes_type` for binary
    data, and `compat.string_types` for when either will do
  - also added `compat.unicode_to_bytes()` and `compat.bytes_to_unicode()` functions,
    for converting between string types

#### Fixed:

- Fixed document(s) removal from `TextCorpus` objects, including correct decrementing
  of `.n_docs`, `.n_sents`, and `.n_tokens` attributes (@michelleful #29)
- Fixed OSError being incorrectly raised in `fileio.open_sesame()` on missing files
- `lang` parameter in `TextDoc` and `TextCorpus` can now be unicode *or* bytes,
  which was bug-like


### 0.2.5 (2016-07-14)

#### Fixed:

- Added (missing) `pyemd` and `python-levenshtein` dependencies to requirements
  and setup files
- Fixed bug in `data.load_depechemood()` arising from the Py2 `csv` module's
  inability to take unicode as input (thanks to @robclewley, issue #25)


### 0.2.4 (2016-07-14)

#### New and Changed:

- New features for `TextDoc` and `TextCorpus` classes
  - added `.save()` methods and `.load()` classmethods, which allows for fast
    serialization of parsed documents/corpora and associated metadata to/from
    disk --- with an important caveat: if `spacy.Vocab` object used to serialize
    and deserialize is not the same, there will be problems, making this format
    useful as short-term but not long-term storage
  - `TextCorpus` may now be instantiated with an already-loaded spaCy pipeline,
    which may or may not have all models loaded; it can still be instantiated
    using a language code string ('en', 'de') to load a spaCy pipeline that
    includes all models by default
  - `TextDoc` methods wrapping `extract` and `keyterms` functions now have full
    documentation rather than forwarding users to the wrapped functions themselves;
    more irritating on the dev side, but much less irritating on the user side :)
- Added a `distance.py` module containing several document, set, and string distance metrics
  - word movers: document distance as distance between individual words represented
    by word2vec vectors, normalized
  - "word2vec": token, span, or document distance as cosine distance between
    (average) word2vec representations, normalized
  - jaccard: string or set(string) distance as intersection / overlap, normalized,
    with optional fuzzy-matching across set members
  - hamming: distance between two strings as number of substititions, optionally
    normalized
  - levenshtein: distance between two strings as number of substitions, deletions,
    and insertions, optionally normalized (and removed a redundant function from
    the still-orphaned `math_utils.py` module)
  - jaro-winkler: distance between two strings with variable prefix weighting, normalized
- Added `most_discriminating_terms()` function to `keyterms` module to take a collection of documents split into two exclusive groups and compute the most discriminating terms for group1-and-not-group2 as well as group2-and-not-group1

#### Fixed:

- fixed variable name error in docs usage example (thanks to @licyeus, PR #23)


### 0.2.3 (2016-06-20)

#### New and Changed:

- Added `corpora.RedditReader()` class for streaming Reddit comments from disk,
  with `.texts()` method for a stream of plaintext comments and `.comments()`
  method for a stream of structured comments as dicts, with basic filtering by
  text length and limiting the number of comments returned
- Refactored functions for streaming Wikipedia articles from disk into a
  `corpora.WikiReader()` class, with `.texts()` method for a stream of plaintext
  articles and `.pages()` method for a stream of structured pages as dicts,
  with basic filtering by text length and limiting the number of pages returned
- Updated README and docs with a more comprehensive --- and correct --- usage example;
  also added tests to ensure it doesn't get stale
- Updated requirements to latest version of spaCy, as well as added matplotlib
  for `viz`

#### Fixed:

- `textacy.preprocess.preprocess_text()` is now, once again, imported at the top
  level, so easily reachable via `textacy.preprocess_text()` (@bretdabaker #14)
- `viz` subpackage now included in the docs' API reference
- missing dependencies added into `setup.py` so pip install handles everything for folks


### 0.2.2 (2016-05-05)

#### New and Changed:

- Added a `viz` subpackage, with two types of plots (so far):
  - `viz.draw_termite_plot()`, typically used to evaluate and interpret topic models;
    conveniently accessible from the `tm.TopicModel` class
  - `viz.draw_semantic_network()` for visualizing networks such as those output
    by `representations.network`
- Added a "Bernie & Hillary" corpus with 3000 congressional speeches made by
  Bernie Sanders and Hillary Clinton since 1996
  - `corpora.fetch_bernie_and_hillary()` function automatically downloads to
    and loads from disk this corpus
- Modified `data.load_depechemood` function, now downloads data from GitHub
  source if not found on disk
- Removed `resources/` directory from GitHub, hence all the downloadin'
- Updated to spaCy v0.100.7
  - German is now supported! although some functionality is English-only
  - added `textacy.load_spacy()` function for loading spaCy packages, taking
    advantage of the new `spacy.load()` API; added a DeprecationWarning for
    `textacy.data.load_spacy_pipeline()`
  - proper nouns' and pronouns' `.pos_` attributes are now correctly assigned
    'PROPN' and 'PRON'; hence, modified `regexes_etc.POS_REGEX_PATTERNS['en']`
    to include 'PROPN'
  - modified `spacy_utils.preserve_case()` to check for language-agnostic
    'PROPN' POS rather than English-specific 'NNP' and 'NNPS' tags
- Added `text_utils.clean_terms()` function for cleaning up a sequence of single-
  or multi-word strings by stripping leading/trailing junk chars, handling
  dangling parens and odd hyphenation, etc.

#### Fixed:

- `textstats.readability_stats()` now correctly gets the number of words in
  a doc from its generator function (@gryBox #8)
- removed NLTK dependency, which wasn't actually required
- `text_utils.detect_language()` now warns via `logging` rather than a
  `print()` statement
- `fileio.write_conll()` documentation now correctly indicates that the filename
  param is not optional


### 0.2.0 (2016-04-11)

#### New and Changed:

- Added `representations` subpackage; includes modules for network and vector
  space model (VSM) document and corpus representations
  - Document-term matrix creation now takes documents represented as a list of
    terms (rather than as spaCy Docs); splits the tokenization step from vectorization
    for added flexibility
  - Some of this functionality was refactored from existing parts of the package
- Added `tm` (topic modeling) subpackage, with a main `TopicModel` class for
  training, applying, persisting, and interpreting NMF, LDA, and LSA topic models
  through a single interface
- Various improvements to `TextDoc` and `TextCorpus` classes
  - `TextDoc` can now be initialized from a spaCy Doc
  - Removed caching from `TextDoc`, because it was a pain and weird and probably
    not all that useful
  - `extract`-based methods are now generators, like the functions they wrap
  - Added `.as_semantic_network()` and `.as_terms_list()` methods to `TextDoc`
  - `TextCorpus.from_texts()` now takes advantage of multithreading via spaCy,
    if available, and document metadata can be passed in as a paired iterable
    of dicts
- Added read/write functions for sparse scipy matrices
- Added `fileio.read.split_content_and_metadata()` convenience function for
  splitting (text) content from associated metadata when reading data from disk
  into a `TextDoc` or `TextCorpus`
- Renamed `fileio.read.get_filenames_in_dir()` to `fileio.read.get_filenames()`
  and added functionality for matching/ignoring files by their names, file extensions,
  and ignoring invisible files
- Rewrote `export.docs_to_gensim()`, now significantly faster
- Imports in `__init__.py` files for main and subpackages now explicit

#### Fixed:

- `textstats.readability_stats()` no longer filters out stop words (@henningko #7)
- Wikipedia article processing now recursively removes nested markup
- `extract.ngrams()` now filters out ngrams with any space-only tokens
- functions with `include_nps` kwarg changed to `include_ncs`, to match the
  renaming of the associated function from `extract.noun_phrases()` to
  `extract.noun_chunks()`


### 0.1.4 (2016-02-26)

#### New:

- Added `corpora` subpackage with `wikipedia.py` module; functions for
  streaming pages from a Wikipedia db dump as plain text or structured data
- Added `fileio` subpackage with functions for reading/writing content from/to
  disk in common formats
  - JSON formats, both standard and streaming-friendly
  - text, optionally compressed
  - spacy documents to/from binary


### 0.1.3 (2016-02-22)

#### New:

- Added `export.py` module for exporting textacy/spacy objects into "third-party"
  formats; so far, just gensim and conll-u
- Added `compat.py` module for Py2/3 compatibility hacks
- Added `TextDoc.merge()` and `spacy_utils.merge_spans()` for merging spans
  into single tokens within a `spacy.Doc`, uses Spacy's recent implementation

#### Changed:

- Renamed `extract.noun_phrases()` to `extract.noun_chunks()` to match Spacy's API
- Changed extract functions to generators, rather than returning lists

#### Fixed:

- Whitespace tokens now always filtered out of `extract.words()` lists
- Some Py2/3 str/unicode issues fixed
- Broken tests in `test_extract.py` no longer broken
