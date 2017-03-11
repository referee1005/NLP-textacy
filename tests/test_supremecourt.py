from __future__ import absolute_import, unicode_literals

import os
import shutil
import tempfile
import unittest

from textacy import __resources_dir__
from textacy.compat import unicode_
from textacy.corpora import supremecourt

CORPUS_FILEPATH = os.path.join(__resources_dir__, 'supremecourt', supremecourt.FILENAME)


@unittest.skipUnless(
    os.path.isfile(CORPUS_FILEPATH), 'SupremeCourt corpus must first be downloaded to run tests')
class SupremeCourtTestCase(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(
            prefix='test_corpora', dir=os.path.dirname(os.path.abspath(__file__)))

    def test_supremecourt_oserror(self):
        self.assertRaises(
            OSError, supremecourt.SupremeCourt,
            self.tempdir, False)

    @unittest.skip("no need to download a fresh corpus every time")
    def test_supremecourt_download(self):
        supremecourt.SupremeCourt(
            data_dir=self.tempdir, download_if_missing=True)
        self.assertTrue(
            os.path.exists(os.path.join(self.tempdir, 'supremecourt', supremecourt.FILENAME)))

    def test_supremecourt_texts(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        for text in cw.texts(limit=3):
            self.assertIsInstance(text, unicode_)

    def test_supremecourt_texts_limit(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        for limit in (1, 5, 100):
            self.assertEqual(sum(1 for _ in cw.texts(limit=limit)), limit)

    def test_supremecourt_texts_min_len(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        for min_len in (100, 200, 1000):
            self.assertTrue(
                all(len(text) >= min_len
                    for text in cw.texts(min_len=min_len, limit=1000)))

    def test_supremecourt_records(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        for record in cw.records(limit=3):
            self.assertIsInstance(record, dict)

    def test_supremecourt_records_opinion_author(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        opinion_authors = ({109}, {113, 114})
        for opinion_author in opinion_authors:
            self.assertTrue(
                all(r['maj_opinion_author'] in opinion_author
                    for r in cw.records(opinion_author=opinion_author, limit=100)))

    def test_supremecourt_records_decision_direction(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        decision_directions = ('liberal', {'conservative', 'unspecifiable'})
        for decision_direction in decision_directions:
            self.assertTrue(
                all(r['decision_direction'] in decision_direction
                    for r in cw.records(decision_direction=decision_direction, limit=100)))

    def test_supremecourt_records_issue_area(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        issue_areas = ({2}, {4, 5, 6})
        for issue_area in issue_areas:
            self.assertTrue(
                all(r['issue_area'] in issue_area
                    for r in cw.records(issue_area=issue_area, limit=100)))

    def test_supremecourt_bad_filters(self):
        cw = supremecourt.SupremeCourt(download_if_missing=False)
        bad_filters = ({'opinion_author': 'Burton DeWilde'},
                       {'opinion_author': 1000},
                       {'decision_direction': 'blatantly political'},
                       {'issue_area': 'legalizing gay marriage, woo!'},
                       {'issue_area': 1000},
                       {'date_range': '2016-01-01'})
        for bad_filter in bad_filters:
            with self.assertRaises(ValueError):
                list(cw._iterate(True, **bad_filter))

    def tearDown(self):
        shutil.rmtree(self.tempdir)
