import pytest

import textacy
from textacy.extract import keyterms as kt


@pytest.fixture(scope="module")
def empty_spacy_doc(lang_en):
    return textacy.make_spacy_doc("", lang=lang_en)


def test_default(doc_long_en):
    result = kt.yake(doc_long_en)
    assert isinstance(result, list) and len(result) > 0
    assert all(isinstance(ts, tuple) and len(ts) == 2 for ts in result)
    assert all(isinstance(ts[0], str) and isinstance(ts[1], float) for ts in result)


def test_normalize_none(doc_long_en):
    result = kt.yake(doc_long_en, normalize=None)
    assert len(result) > 0


def test_normalize_lower(doc_long_en):
    result = kt.yake(doc_long_en, normalize="lower")
    assert len(result) > 0
    assert all(term == term.lower() for term, _ in result)


def test_normalize_lemma(doc_long_en):
    result = kt.yake(doc_long_en, normalize="lemma")
    assert len(result) > 0
    assert any(term != term.lower() for term, _ in result)


def test_normalize_norm(doc_long_en):
    result = kt.yake(doc_long_en, normalize="norm")
    assert len(result) > 0


def test_ngrams_1(doc_long_en):
    result = kt.yake(doc_long_en, ngrams=1)
    assert len(result) > 0
    assert all(len(term.split()) == 1 for term, _ in result)


def test_ngrams_2_3(doc_long_en):
    result = kt.yake(doc_long_en, ngrams=(2, 3))
    assert len(result) > 0
    assert all(2 <= len(term.split()) <= 3 for term, _ in result)


def test_n_topn(doc_long_en):
    for n in (5, 25):
        result = kt.yake(doc_long_en, topn=n)
        assert 0 < len(result) <= n


def test_topn_float(doc_long_en):
    result = kt.yake(doc_long_en, topn=0.2)
    assert len(result) > 0
    with pytest.raises(ValueError):
        _ = kt.yake(doc_long_en, topn=2.0)


def test_window_size(doc_long_en):
    result_2 = kt.yake(doc_long_en, window_size=2)
    result_4 = kt.yake(doc_long_en, window_size=4)
    assert len(result_2) > 0 and len(result_4) > 0
    assert result_2 != result_4


def test_empty_doc(empty_spacy_doc):
    result = kt.yake(empty_spacy_doc)
    assert isinstance(result, list)
    assert len(result) == 0
