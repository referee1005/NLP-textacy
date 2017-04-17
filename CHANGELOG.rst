Changelog
=========

0.3.4 (2017-04-17)
------------------

Changes:

- Improved and expanded calculation of basic counts and readability statistics in ``text_stats`` module.
    - Added a ``TextStats()`` class for more convenient, granular access to individual values. See usage docs for more info. When calculating, say, just one readability statistic, performance with this class should be slightly better; if calculating _all_ statistics, performance is worse owing to unavoidable, added overhead in Python for variable lookups. The legacy function ``text_stats.readability_stats()`` still exists and behaves as before, but a deprecation warning is displayed.
    - Added functions for calculating Wiener Sachtextformel (PR #77), LIX, and GULPease readability statistics.
    - Added number of long words and number of monosyllabic words to basic counts.
- Clarified the need for having spacy models installed for most use cases of textacy, in addition to just the spacy package.
    - README updated with comments on this, including links to more extensive spacy documentation. (Issues #66 and #68)
    - Added a function, ``compat.get_config()`` that includes information about which (if any) spacy models are installed.
    - Recent changes to spacy, including a warning message, will also make model problems more apaprent.
- Added an ``ngrams`` parameter to ``keyterms.sgrank()``, allowing for more flexibility in specifying valid keyterm candidates for the algorithm. (PR #75)
- Dropped dependency on ``fuzzywuzzy`` package, replacing usage of ``fuzz.token_sort_ratio()`` with a textacy equivalent in order to avoid license incompatibilities. As a bonus, the new code seems to perform faster! (Issue #62)
    - Note: Outputs are now floats in [0.0, 1.0], consistent with other similarity functions, whereas before outputs were ints in [0, 100]. This has implications for ``match_threshold`` values passed to ``similarity.jaccard()``; a warning is displayed and the conversion is performed automatically, for now.
- A MANIFEST.in file was added to include docs, tests, and distribution files in the source distribution. This is just good practice. (PR #65)

Bugfixes:

- Known acronym-definition pairs are now properly handled in ``extract.acronyms_and_definitions()`` (Issue #61)
- WikiReader no longer crashes on null page element content while parsing (PR #64)
- Fixed a rare but perfectly legal edge case exception in ``keyterms.sgrank()``, and added a window width sanity check. (Issue #72)
- Fixed assignment of 2-letter language codes to ``Doc`` and ``Corpus`` objects when the lang parameter is specified as a full spacy model name.
- Replaced several leftover print statements with proper logging functions.

Contributors:

Big thanks to @oroszgy, @rolando, @covuworie, and @RolandColored for the pull requests!


0.3.3 (2017-02-10)
------------------

Changes:

- Added a consistent ``normalize`` param to functions and methods that require token/span text normalization. Typically, it takes one of the following values: 'lemma' to lemmatize tokens, 'lower' to lowercase tokens, False-y to *not* normalize tokens, or a function that converts a spacy token or span into a string, in whatever way the user prefers (e.g. ``spacy_utils.normalized_str()``).
    - Functions modified to use this param: ``Doc.to_bag_of_terms()``, ``Doc.to_bag_of_words()``, ``Doc.to_terms_list()``, ``Doc.to_semantic_network()``, ``Corpus.word_freqs()``, ``Corpus.word_doc_freqs()``, ``keyterms.sgrank()``, ``keyterms.textrank()``, ``keyterms.singlerank()``, ``keyterms.key_terms_from_semantic_network()``, ``network.terms_to_semantic_network()``, ``network.sents_to_semantic_network()``,
- Tweaked ``keyterms.sgrank()`` for higher quality results and improved internal performance.
- When getting both n-grams and named entities with ``Doc.to_terms_list()``, filtering out numeric spans for only one is automatically extended to the other. This prevents unexpected behavior, such as passing `filter_nums=True` but getting numeric named entities back in the terms list.

Bufixes:

- ``keyterms.sgrank()`` no longer crashes if a term is missing from ``idfs`` mapping. (@jeremybmerrill, issue #53)
- Proper nouns are no longer excluded from consideration as keyterms in ``keyterms.sgrank()`` and ``keyterms.textrank()``. (@jeremybmerrill, issue #53)
- Empty strings are now excluded from consideration as keyterms — a bug inherited from spaCy. (@mlehl88, issue #58)


0.3.2 (2016-11-15)
------------------

Changes:

- Preliminary inclusion of custom spaCy pipelines
    - updated ``load_spacy()`` to include explicit path and create_pipeline kwargs, and removed the already-deprecated ``load_spacy_pipeline()`` function to avoid confusion around spaCy languages and pipelines
    - added ``spacy_pipelines`` module to hold implementations of custom spaCy pipelines, including a basic one that merges entities into single tokens
    - note: necessarily bumped minimum spaCy version to 1.1.0+
    - see the announcement here: https://explosion.ai/blog/spacy-deep-learning-keras
- To reduce code bloat, made the ``matplotlib`` dependency optional and dropped the ``gensim`` dependency
    - to install ``matplotlib`` at the same time as textacy, do ``$ pip install textacy[viz]``
    - bonus: ``backports.csv`` is now only installed for Py2 users
    - thanks to @mbatchkarov for the request
- Improved performance of ``textacy.corpora.WikiReader().texts()``; results should stream faster and have cleaner plaintext content than when they were produced by ``gensim``
    - this *should* also fix a bug reported in Issue #51 by @baisk
- Added a ``Corpus.vectors`` property that returns a matrix of shape (# documents, vector dim) containing the average word2vec-style vector representation of constituent tokens for all ``Doc`` s


0.3.1 (2016-10-19)
------------------

Changes:

- Updated spaCy dependency to the latest v1.0.1; set a floor on other dependencies' versions to make sure everyone's running reasonably up-to-date code


Bugfixes:

- Fixed incorrect kwarg in `sgrank` 's call to `extract.ngrams()` (@patcollis34, issue #44)
- Fixed import for `cachetool` 's `hashkey`, which changed in the v2.0 (@gramonov, issue #45)


0.3.0 (2016-08-23)
------------------

Changes:

- Refactored and streamlined `TextDoc`; changed name to `Doc`
    - simplified init params: `lang` can now be a language code string or an equivalent `spacy.Language` object, and `content` is either a string or `spacy.Doc`; param values and their interactions are better checked for errors and inconsistencies
    - renamed and improved methods transforming the Doc; for example, `.as_bag_of_terms()` is now `.to_bag_of_terms()`, and terms can be returned as integer ids (default) or as strings with absolute, relative, or binary frequencies as weights
    - added performant `.to_bag_of_words()` method, at the cost of less customizability of what gets included in the bag (no stopwords or punctuation); words can be returned as integer ids (default) or as strings with absolute, relative, or binary frequencies as weights
    - removed methods wrapping `extract` functions, in favor of simply calling that function on the Doc (see below for updates to `extract` functions to make this more convenient); for example, `TextDoc.words()` is now `extract.words(Doc)`
    - removed `.term_counts()` method, which was redundant with `Doc.to_bag_of_terms()`
    - renamed `.term_count()` => `.count()`, and checking + caching results is now smarter and faster
- Refactored and streamlined `TextCorpus`; changed name to `Corpus`
    - added init params: can now initialize a `Corpus` with a stream of texts, spacy or textacy Docs, and optional metadatas, analogous to `Doc`; accordingly, removed `.from_texts()` class method
    - refactored, streamlined, *bug-fixed*, and made consistent the process of adding, getting, and removing documents from `Corpus`
        - getting/removing by index is now equivalent to the built-in `list` API: `Corpus[:5]` gets the first 5 `Doc`s, and `del Corpus[:5]` removes the first 5, automatically keeping track of corpus statistics for total # docs, sents, and tokens
        - getting/removing by boolean function is now done via the `.get()` and `.remove()` methods, the latter of which now also correctly tracks corpus stats
        - adding documents is split across the `.add_text()`, `.add_texts()`, and `.add_doc()` methods for performance and clarity reasons
    - added `.word_freqs()` and `.word_doc_freqs()` methods for getting a mapping of word (int id or string) to global weight (absolute, relative, binary, or inverse frequency); akin to a vectorized representation (see: `textacy.vsm`) but in non-vectorized form, which can be useful
    - removed `.as_doc_term_matrix()` method, which was just wrapping another function; so, instead of `corpus.as_doc_term_matrix((doc.as_terms_list() for doc in corpus))`, do `textacy.vsm.doc_term_matrix((doc.to_terms_list(as_strings=True) for doc in corpus))`
- Updated several `extract` functions
    - almost all now accept either a `textacy.Doc` or `spacy.Doc` as input
    - renamed and improved parameters for filtering for or against certain POS or NE types; for example, `good_pos_tags` is now `include_pos`, and will accept either a single POS tag as a string or a set of POS tags to filter for; same goes for `exclude_pos`, and analogously `include_types`, and `exclude_types`
- Updated corpora classes for consistency and added flexibility
    - enforced a consistent API: `.texts()` for a stream of plain text documents and `.records()` for a stream of dicts containing both text and metadata
    - added filtering options for `RedditReader`, e.g. by date or subreddit, consistent with other corpora (similar tweaks to `WikiReader` may come later, but it's slightly more complicated...)
    - added a nicer `repr` for `RedditReader` and `WikiReader` corpora, consistent with other corpora
- Moved `vsm.py` and `network.py` into the top-level of `textacy` and thus removed the `representations` subpackage
    - renamed `vsm.build_doc_term_matrix()` => `vsm.doc_term_matrix()`, because the "build" part of it is obvious
- Renamed `distance.py` => `similarity.py`; all returned values are now similarity metrics in the interval [0, 1], where higher values indicate higher similarity
- Renamed `regexes_etc.py` => `constants.py`, without additional changes
- Renamed `fileio.utils.split_content_and_metadata()` => `fileio.utils.split_record_fields()`, without further changes (except for tweaks to the docstring)
- Added functions to read and write delimited file formats: `fileio.read_csv()` and `fileio.write_csv()`, where the delimiter can be any valid one-char string; gzip/bzip/lzma compression is handled automatically when available
- Added better and more consistent docstrings and usage examples throughout the code base


0.2.8 (2016-08-03)
------------------

Changes:

- Added two new corpora!
    - the CapitolWords corpus: a collection of 11k speeches (~7M tokens) given by the main protagonists of the 2016 U.S. Presidential election that had previously served in the U.S. Congress — including Hillary Clinton, Bernie Sanders, Barack Obama, Ted Cruz, and John Kasich — from January 1996 through June 2016
    - the SupremeCourt corpus: a collection of 8.4k court cases (~71M tokens) decided by the U.S. Supreme Court from 1946 through 2016, with metadata on subject matter categories, ideology, and voting patterns
    - **DEPRECATED:** the Bernie and Hillary corpus, which is a small subset of CapitolWords that can be easily recreated by filtering CapitolWords by `speaker_name={'Bernie Sanders', 'Hillary Clinton'}`
- Refactored and improved `fileio` subpackage
    - moved shared (read/write) functions into separate `fileio.utils` module
    - almost all read/write functions now use `fileio.utils.open_sesame()`, enabling seamless fileio for uncompressed or gzip, bz2, and lzma compressed files; relative/user-home-based paths; and missing intermediate directories. NOTE: certain file mode / compression pairs simply don't work (this is Python's fault), so users may run into exceptions; in Python 3, you'll almost always want to use text mode ('wt' or 'rt'), but in Python 2, users can't read or write compressed files in text mode, only binary mode ('wb' or 'rb')
    - added options for writing json files (matching stdlib's `json.dump()`) that can help save space
    - `fileio.utils.get_filenames()` now matches for/against a regex pattern rather than just a contained substring; using the old params will now raise a deprecation warning
    - **BREAKING:** `fileio.utils.split_content_and_metadata()` now has `itemwise=False` by default, rather than `itemwise=True`, which means that splitting multi-document streams of content and metadata into parallel iterators is now the default action
    - added `compression` param to `TextCorpus.save()` and `.load()` to optionally write metadata json file in compressed form
    - moved `fileio.write_conll()` functionality to `export.doc_to_conll()`, which converts a spaCy doc into a ConLL-U formatted string; writing that string to disk would require a separate call to `fileio.write_file()`
- Cleaned up deprecated/bad Py2/3 `compat` imports, and added better functionality for Py2/3 strings
    - now `compat.unicode_type` used for text data, `compat.bytes_type` for binary data, and `compat.string_types` for when either will do
    - also added `compat.unicode_to_bytes()` and `compat.bytes_to_unicode()` functions, for converting between string types

Bugfixes:

- Fixed document(s) removal from `TextCorpus` objects, including correct decrementing of `.n_docs`, `.n_sents`, and `.n_tokens` attributes (@michelleful #29)
- Fixed OSError being incorrectly raised in `fileio.open_sesame()` on missing files
- `lang` parameter in `TextDoc` and `TextCorpus` can now be unicode *or* bytes, which was bug-like


0.2.5 (2016-07-14)
------------------

Bugfixes:

- Added (missing) `pyemd` and `python-levenshtein` dependencies to requirements and setup files
- Fixed bug in `data.load_depechemood()` arising from the Py2 `csv` module's inability to take unicode as input (thanks to @robclewley, issue #25)


0.2.4 (2016-07-14)
------------------

Changes:

- New features for `TextDoc` and `TextCorpus` classes
    - added `.save()` methods and `.load()` classmethods, which allows for fast serialization of parsed documents/corpora and associated metadata to/from disk — with an important caveat: if `spacy.Vocab` object used to serialize and deserialize is not the same, there will be problems, making this format useful as short-term but not long-term storage
    - `TextCorpus` may now be instantiated with an already-loaded spaCy pipeline, which may or may not have all models loaded; it can still be instantiated using a language code string ('en', 'de') to load a spaCy pipeline that includes all models by default
    - `TextDoc` methods wrapping `extract` and `keyterms` functions now have full documentation rather than forwarding users to the wrapped functions themselves; more irritating on the dev side, but much less irritating on the user side :)
- Added a `distance.py` module containing several document, set, and string distance metrics
    - word movers: document distance as distance between individual words represented by word2vec vectors, normalized
    - "word2vec": token, span, or document distance as cosine distance between (average) word2vec representations, normalized
    - jaccard: string or set(string) distance as intersection / overlap, normalized, with optional fuzzy-matching across set members
    - hamming: distance between two strings as number of substititions, optionally normalized
    - levenshtein: distance between two strings as number of substitions, deletions, and insertions, optionally normalized (and removed a redundant function from the still-orphaned `math_utils.py` module)
    - jaro-winkler: distance between two strings with variable prefix weighting, normalized
- Added `most_discriminating_terms()` function to `keyterms` module to take a collection of documents split into two exclusive groups and compute the most discriminating terms for group1-and-not-group2 as well as group2-and-not-group1

Bugfixes:

- fixed variable name error in docs usage example (thanks to @licyeus, PR #23)


0.2.3 (2016-06-20)
------------------

Changes:

- Added `corpora.RedditReader()` class for streaming Reddit comments from disk, with `.texts()` method for a stream of plaintext comments and `.comments()` method for a stream of structured comments as dicts, with basic filtering by text length and limiting the number of comments returned
- Refactored functions for streaming Wikipedia articles from disk into a `corpora.WikiReader()` class, with `.texts()` method for a stream of plaintext articles and `.pages()` method for a stream of structured pages as dicts, with basic filtering by text length and limiting the number of pages returned
- Updated README and docs with a more comprehensive — and correct — usage example; also added tests to ensure it doesn't get stale
- Updated requirements to latest version of spaCy, as well as added matplotlib for `viz`

Bugfixes:

- `textacy.preprocess.preprocess_text()` is now, once again, imported at the top level, so easily reachable via `textacy.preprocess_text()` (@bretdabaker #14)
- `viz` subpackage now included in the docs' API reference
- missing dependencies added into `setup.py` so pip install handles everything for folks


0.2.2 (2016-05-05)
------------------

Changes:

- Added a `viz` subpackage, with two types of plots (so far):
    - `viz.draw_termite_plot()`, typically used to evaluate and interpret topic models; conveniently accessible from the `tm.TopicModel` class
    - `viz.draw_semantic_network()` for visualizing networks such as those output by `representations.network`
- Added a "Bernie & Hillary" corpus with 3000 congressional speeches made by Bernie Sanders and Hillary Clinton since 1996
    - ``corpora.fetch_bernie_and_hillary()`` function automatically downloads to and loads from disk this corpus
- Modified ``data.load_depechemood`` function, now downloads data from GitHub source if not found on disk
- Removed ``resources/`` directory from GitHub, hence all the downloadin'
- Updated to spaCy v0.100.7
    - German is now supported! although some functionality is English-only
    - added `textacy.load_spacy()` function for loading spaCy packages, taking advantage of the new `spacy.load()` API; added a DeprecationWarning for `textacy.data.load_spacy_pipeline()`
    - proper nouns' and pronouns' ``.pos_`` attributes are now correctly assigned 'PROPN' and 'PRON'; hence, modified ``regexes_etc.POS_REGEX_PATTERNS['en']`` to include 'PROPN'
    - modified ``spacy_utils.preserve_case()`` to check for language-agnostic 'PROPN' POS rather than English-specific 'NNP' and 'NNPS' tags
- Added `text_utils.clean_terms()` function for cleaning up a sequence of single- or multi-word strings by stripping leading/trailing junk chars, handling dangling parens and odd hyphenation, etc.

Bugfixes:

- ``textstats.readability_stats()`` now correctly gets the number of words in a doc from its generator function (@gryBox #8)
- removed NLTK dependency, which wasn't actually required
- ``text_utils.detect_language()`` now warns via ``logging`` rather than a ``print()`` statement
- ``fileio.write_conll()`` documentation now correctly indicates that the filename param is not optional


0.2.0 (2016-04-11)
------------------

Changes:

- Added ``representations`` subpackage; includes modules for network and vector space model (VSM) document and corpus representations
    - Document-term matrix creation now takes documents represented as a list of terms (rather than as spaCy Docs); splits the tokenization step from vectorization for added flexibility
    - Some of this functionality was refactored from existing parts of the package
- Added ``tm`` (topic modeling) subpackage, with a main ``TopicModel`` class for training, applying, persisting, and interpreting NMF, LDA, and LSA topic models through a single interface
- Various improvements to ``TextDoc`` and ``TextCorpus`` classes
    - ``TextDoc`` can now be initialized from a spaCy Doc
    - Removed caching from ``TextDoc``, because it was a pain and weird and probably not all that useful
    - ``extract``-based methods are now generators, like the functions they wrap
    - Added ``.as_semantic_network()`` and ``.as_terms_list()`` methods to ``TextDoc``
    - ``TextCorpus.from_texts()`` now takes advantage of multithreading via spaCy, if available, and document metadata can be passed in as a paired iterable of dicts
- Added read/write functions for sparse scipy matrices
- Added ``fileio.read.split_content_and_metadata()`` convenience function for splitting (text) content from associated metadata when reading data from disk into a ``TextDoc`` or ``TextCorpus``
- Renamed ``fileio.read.get_filenames_in_dir()`` to ``fileio.read.get_filenames()`` and added functionality for matching/ignoring files by their names, file extensions, and ignoring invisible files
- Rewrote ``export.docs_to_gensim()``, now significantly faster
- Imports in ``__init__.py`` files for main and subpackages now explicit

Bugfixes:

- ``textstats.readability_stats()`` no longer filters out stop words (@henningko #7)
- Wikipedia article processing now recursively removes nested markup
- ``extract.ngrams()`` now filters out ngrams with any space-only tokens
- functions with ``include_nps`` kwarg changed to ``include_ncs``, to match the renaming of the associated function from ``extract.noun_phrases()`` to ``extract.noun_chunks()``

0.1.4 (2016-02-26)
------------------

Changes:

- Added ``corpora`` subpackage with ``wikipedia.py`` module; functions for streaming pages from a Wikipedia db dump as plain text or structured data
- Added ``fileio`` subpackage with functions for reading/writing content from/to disk in common formats
  - JSON formats, both standard and streaming-friendly
  - text, optionally compressed
  - spacy documents to/from binary

0.1.3 (2016-02-22)
------------------

Changes:

- Added ``export.py`` module for exporting textacy/spacy objects into "third-party" formats; so far, just gensim and conll-u
- Added ``compat.py`` module for Py2/3 compatibility hacks
- Renamed ``extract.noun_phrases()`` to ``extract.noun_chunks()`` to match Spacy's API
- Changed extract functions to generators, rather than returning lists
- Added ``TextDoc.merge()`` and ``spacy_utils.merge_spans()`` for merging spans into single tokens within a ``spacy.Doc``, uses Spacy's recent implementation

Bug fixes:

- Whitespace tokens now always filtered out of ``extract.words()`` lists
- Some Py2/3 str/unicode issues fixed
- Broken tests in ``test_extract.py`` no longer broken
