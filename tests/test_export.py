import re

import numpy as np
import pytest

from textacy import load_spacy_lang
from textacy import export


@pytest.fixture(scope="module")
def spacy_doc():
    text = "I would have lived in peace. But my enemies brought me war."
    spacy_lang = load_spacy_lang("en")
    spacy_doc = spacy_lang(text)
    return spacy_doc


def test_to_gensim(spacy_doc):
    spacy_lang = load_spacy_lang("en")
    result = export.docs_to_gensim(
        [spacy_doc], spacy_lang.vocab,
        filter_stops=True, filter_punct=True, filter_nums=True,
    )
    assert isinstance(result[0], str)
    assert isinstance(result[1], list)
    assert isinstance(result[1][0], list)
    assert isinstance(result[1][0][0], tuple)
    assert (
        isinstance(result[1][0][0][0], int)
        and isinstance(result[1][0][0][1], int)
    )


def test_write_conll(spacy_doc):
    result = export.doc_to_conll(spacy_doc)
    assert len(re.findall(r"^# sent_id \d$", result, flags=re.MULTILINE)) == 2
    assert all(
        line.count("\t") == 9
        for line in result.split("\n")
        if re.search(r"^\d+\s", line)
    )
    assert all(
        line == re.search(r"\d+\s([\w=\.\$\-]+\s?)+", line).group()
        for line in result.split("\n")
        if re.search(r"^\d+\s", line)
    )
