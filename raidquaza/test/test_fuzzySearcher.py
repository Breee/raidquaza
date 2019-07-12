#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from search.fuzzysearch import FuzzySearcher
from search.enums import RECORD_TYPE
import test.testconfig as config

fuzzy = FuzzySearcher(config=config)


class TestFuzzySearcher(TestCase):

    def test_index(self):
        expected_inverted_lists = {'$$g': [0, 1], '$gr': [0], 'grö': [0], 'rös': [0], 'öss': [0], 'sst': [0],
                                   'ste': [0], 'tep': [0], 'epf': [0],
                                   'pfe': [0], 'fei': [0], 'eif': [0], 'ife': [0], 'few': [0], 'ewa': [0], 'wal': [0],
                                   'ald': [0], 'ldk': [0],
                                   'dki': [0], 'kir': [0, 4, 6], 'irc': [0, 4, 6], 'rch': [0, 4, 6], 'chs': [0],
                                   'hs$': [0], 's$$': [0, 5],
                                   '$gu': [1], 'gut': [1], 'utl': [1], 'tle': [1], 'leu': [1], 'eut': [1], 'utk': [1],
                                   'tkr': [1], 'kre': [1],
                                   'rei': [1], 'eis': [1], 'is1': [1], 's1$': [1], '1$$': [1], '$$s': [2, 5],
                                   '$so': [2], 'son': [2], 'onn': [2],
                                   'nne': [2, 6], 'nen': [2], 'enu': [2], 'nuh': [2], 'uhr': [2], 'hrs': [2],
                                   'rst': [2], 'sta': [2], 'tau': [2],
                                   'aud': [2], 'udi': [2], 'din': [2], 'ing': [2], 'nge': [2], 'ger': [2], 'er$': [2],
                                   'r$$': [2], '$$b': [3],
                                   '$be': [3], 'bea': [3], 'eat': [3], 'atm': [3], 'tma': [3], 'man': [3], 'anh': [3],
                                   'nha': [3], 'has': [3],
                                   'asl': [3], 'sla': [3], 'lac': [3], 'ach': [3], 'ch$': [3], 'h$$': [3], '$$m': [4],
                                   '$me': [4], 'mel': [4],
                                   'ela': [4], 'lan': [4], 'anc': [4], 'nch': [4], 'cht': [4], 'hth': [4], 'tho': [4],
                                   'hon': [4], 'onk': [4],
                                   'nki': [4], 'che': [4, 6], 'he$': [4, 6], 'e$$': [4, 6], '$sc': [5], 'sch': [5],
                                   'chl': [5], 'hlo': [5],
                                   'los': [5], 'oss': [5, 5], 'ssb': [5], 'sbe': [5], 'ber': [5], 'erg': [5],
                                   'rgc': [5], 'gcr': [5], 'cro': [5],
                                   'ros': [5], 'ss$': [5], '$$j': [6], '$jo': [6], 'joh': [6], 'oha': [6], 'han': [6],
                                   'ann': [6], 'nes': [6],
                                   'esk': [6], 'ski': [6]
                                   }
        expected_longitude = ['7.953323', '7.820795', '7.825398', '7.826742', '7.817412', '7.858673', '7.847594']
        expected_latitude = ['48.091214', '47.988518', '47.991222', '47.991146', '47.992087', '47.994854', '47.988868']
        expected_vocab = {0: 'Grösste Pfeife Waldkirchs', 1: 'Gutleutkreis 1', 2: 'Sonnenuhr Staudinger',
                          3: 'Beat Man Haslach', 4: 'Melanchthonkirche', 5: 'Schlossberg Cross', 6: 'Johanneskirche'
                          }
        expected_types = [RECORD_TYPE.GYM, RECORD_TYPE.GYM, RECORD_TYPE.GYM, RECORD_TYPE.POKESTOP, RECORD_TYPE.POKESTOP,
                          RECORD_TYPE.GYM, RECORD_TYPE.GYM]

        self.assertEqual(fuzzy.point_of_interest_index.inverted_lists, expected_inverted_lists)
        self.assertEqual(fuzzy.point_of_interest_index.latitude, expected_latitude)
        self.assertEqual(fuzzy.point_of_interest_index.longitude, expected_longitude)
        self.assertEqual(fuzzy.point_of_interest_index.vocab, expected_vocab)
        self.assertEqual(fuzzy.point_of_interest_index.types, expected_types)

    def test_search(self):
        # Test: if a query matches a record, the record shall be the #1 result.
        full_match_query_list = {0: 'Grösste Pfeife Waldkirchs', 1: 'Gutleutkreis 1', 2: 'Sonnenuhr Staudinger',
                                 3: 'Beat Man Haslach', 4: 'Melanchthonkirche', 5: 'Schlossberg Cross',
                                 6: 'Johanneskirche'
                                 }
        expected_scores = [-66.0, -36.0, -54.0, -39.0, -48.0, -45.0, -39.0]
        for record_id, record in full_match_query_list.items():
            result = fuzzy.search(query=record, num_results=1)
            expected_result = [(fuzzy.point_of_interest_index.vocab[record_id],
                                (fuzzy.point_of_interest_index.latitude[record_id],
                                 fuzzy.point_of_interest_index.longitude[record_id]),
                                fuzzy.point_of_interest_index.types[record_id],
                                expected_scores[record_id])]
            self.assertEqual(result, expected_result)
