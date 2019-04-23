from __future__ import absolute_import, unicode_literals

import os

import pytest

from textacy import compat
from textacy.datasets.oxford_text_archive import OxfordTextArchive

DATASET = OxfordTextArchive()

pytestmark = pytest.mark.skipif(
    DATASET.metadata is None,
    reason="OxfordTextArchive dataset must be downloaded before running tests",
)


@pytest.mark.skip("No need to download a new dataset every time")
def test_download(tmpdir):
    dataset = OxfordTextArchive(data_dir=str(tempdir))
    dataset.download()
    assert os.path.exists(dataset.metadata)
    assert os.path.exists(dataset._metadata_filepath)
    assert os.path.exists(dataset._text_dirpath)


def test_oserror(tmpdir):
    dataset = OxfordTextArchive(data_dir=str(tmpdir))
    with pytest.raises(OSError):
        _ = list(dataset.texts())


def test_texts():
    for text in DATASET.texts(limit=3):
        assert isinstance(text, compat.unicode_)


def test_texts_limit():
    for limit in (1, 5, 100):
        assert sum(1 for _ in DATASET.texts(limit=limit)) == limit


def test_texts_min_len():
    for min_len in (100, 200, 1000):
        assert all(
            len(text) >= min_len for text in DATASET.texts(min_len=min_len, limit=10)
        )


def test_records():
    for text, meta in DATASET.records(limit=3):
        assert isinstance(text, compat.unicode_)
        assert isinstance(meta, dict)


def test_records_author():
    authors = ({"Shakespeare, William"}, {"Wollstonecraft, Mary", "Twain, Mark"})
    for author in authors:
        assert all(
            athr in author
            for text, meta in DATASET.records(author=author, limit=3)
            for athr in meta["author"]
        )


def test_records_date_range():
    date_ranges = (["1900-01-01", "1950-01-01"], ("1600-01-01", "1700-01-01"))
    for date_range in date_ranges:
        assert all(
            date_range[0] <= meta["year"] < date_range[1]
            for text, meta in DATASET.records(date_range=date_range, limit=10)
        )


def test_bad_filters():
    bad_filters = ({"author": "Burton DeWilde"}, {"date_range": "2016-01-01"})
    for bad_filter in bad_filters:
        with pytest.raises(ValueError):
            list(DATASET.texts(**bad_filter))
