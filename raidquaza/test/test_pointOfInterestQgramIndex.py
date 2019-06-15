import csv
from unittest import TestCase
from search.qgram_index import PointOfInterestQgramIndex
from search.enums import RECORD_TYPE

index = PointOfInterestQgramIndex(q=3, use_geofences=False, channel_to_geofences=dict())
test_data = 'test_data.csv'


class TestPointOfInterestQgramIndex(TestCase):

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
        expected_latitude = ['48.091214', '47.988518', '47.991222', '47.991146', '47.992087', '47.994854', '47.988868']
        expected_longitude = ['7.953323', '7.820795', '7.825398', '7.826742', '7.817412', '7.858673', '7.847594']
        expected_vocab = {0: 'Grösste Pfeife Waldkirchs', 1: 'Gutleutkreis 1', 2: 'Sonnenuhr Staudinger',
                          3: 'Beat Man Haslach', 4: 'Melanchthonkirche', 5: 'Schlossberg Cross', 6: 'Johanneskirche'
                          }
        expected_types = [RECORD_TYPE.GYM, RECORD_TYPE.GYM, RECORD_TYPE.GYM, RECORD_TYPE.POKESTOP, RECORD_TYPE.POKESTOP,
                          RECORD_TYPE.GYM, RECORD_TYPE.GYM]

        self.assertEqual(index.inverted_lists, expected_inverted_lists)
        self.assertEqual(index.longitude, expected_longitude)
        self.assertEqual(index.latitude, expected_latitude)
        self.assertEqual(index.vocab, expected_vocab)
        self.assertEqual(index.types, expected_types)

    def test_build_from_file(self):
        index.build_from_file(test_data)
        self.test_index()

    def csv_to_list(self, file):
        records = []
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader, None)  # skip the header
            for row in reader:
                records.append((row[0].strip(), row[1].strip(), row[2].strip(),
                                RECORD_TYPE.GYM if row[3].strip() == 'Gym' else RECORD_TYPE.POKESTOP))
        return records

    def test_build_from_lists(self):
        # list which contains tuples of the form (name,lat,lon,type)    
        index.build_from_lists(input=self.csv_to_list(test_data))
        self.test_index()

    def test_get_posting_list(self):
        index.build_from_file(test_data)
        qgrams = ['dki', 'kir', 'irc', 'rch', 'chs']
        expected_posting_lists = [[0], [0, 4, 6], [0, 4, 6], [0, 4, 6], [0]]
        for i, qgram in enumerate(qgrams):
            acutal_posting_list = index.get_posting_list(qgram)
            self.assertAlmostEqual(acutal_posting_list, expected_posting_lists[i])

    def test_get_score(self):
        words = ['Grösste Pfeife Waldkirchs', 'Gutleutkreis 1', 'Sonnenuhr Staudinger', 'Beat Man Haslach',
                 'Melanchthonkirche', 'Schlossberg Cross', 'Johanneskirche']
        queries_full_match = ['Grösste Pfeife Waldkirchs', 'Gutleutkreis 1', 'Sonnenuhr Staudinger', 'Beat Man Haslach',
                              'Melanchthonkirche', 'Schlossberg Cross', 'Johanneskirche']
        scores_full_match = [-72.0, -39.0, -57.0, -45.0, -48.0, -48.0, -39.0]

        queries_typos = ['Grössde feife Waldmirchs', 'Gutmeutkreiss 1', 'Sonnenuhr Laudinger', 'Beat Man Hasfach',
                         'Melanchthon', 'Schlossgferg Cross', 'Johanneslirrche']

        for word, query in zip(words, queries_full_match):
            scores_full_match.append(index.get_score(query, word))
        print(scores_full_match)

    def check_query_results(self, queries, target_records):
        for query, target in zip(queries, target_records):
            matches = [x[0] for x in index.find_matches(query, k=5)]
            print(f"query: {query}, target:{target}, matches: {matches}")
            self.assertIn(target, matches)

    def test_find_matches(self):
        index.build_from_file(test_data)
        target_records = ['Grösste Pfeife Waldkirchs', 'Gutleutkreis 1', 'Sonnenuhr Staudinger', 'Beat Man Haslach',
                          'Melanchthonkirche', 'Schlossberg Cross', 'Johanneskirche']

        queries_full_match = ['Grösste Pfeife Waldkirchs', 'Gutleutkreis 1', 'Sonnenuhr Staudinger', 'Beat Man Haslach',
                              'Melanchthonkirche', 'Schlossberg Cross', 'Johanneskirche']

        queries_typos = ['Grössde feife Waldmirchs', 'Gutmeutkreiss 1', 'Sonnenuhr Laudinger', 'Beat Man Hasfach',
                         'Melanchthon', 'Schlossgferg Cross', 'Johanneslirrche']

        self.check_query_results(queries_full_match, target_records)
        self.check_query_results(queries_typos, target_records)
