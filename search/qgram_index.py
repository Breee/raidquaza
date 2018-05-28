"""
Copyright 2015, University of Freiburg.
Chair of Algorithms and Data Structures.
Elmar Haussmann <haussmann@cs.uni-freiburg.de>
Julian Löffler <Loeffler.uni@gmail.com>
"""

import sys
import time
import re
import numpy as np
from collections import Counter
import math
from enum import Enum

class SCORING_TYPE(Enum):
    LEVENSHTEIN = 1,
    NEEDLEMAN_WUNSCH = 2,
    AFFINE_GAPS = 3


def get_qgrams(str, q):
    """ Returns all q-grams for str.
        >>> get_qgrams("bananarana", 3)
        ['$$b', '$ba', 'ban', 'ana', 'nan', 'ana', 'nar', 'ara', 'ran', 'ana', 'na$', 'a$$']
        >>> get_qgrams("b", 3)
        ['$$b', '$b$', 'b$$']
        >>> get_qgrams("ba", 4)
        ['$$$b', '$$ba', '$ba$', 'ba$$', 'a$$$']
        >>> get_qgrams("banana", 2)
        ['$b', 'ba', 'an', 'na', 'an', 'na', 'a$']
        """
    str = "$" * (q - 1) + str + "$" * (q - 1)
    qgrams = []
    for i in range(0, len(str) - q + 1):
        qgram = str[i:i + q]
        qgrams.append(qgram)
    return qgrams


def merge(lists):
    """ Merge the inverted lists and return a list of tuples (record id,
        count). Alternatively, you can also return a dictionary from record ids
        to counts.
        >>> merge([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        [(1, 1), (2, 2), (3, 3), (4, 2), (5, 1)]
        >>> merge([[1, 3, 4, 6, 7], [1, 3, 4, 5, 6, 7, 10]])
        [(1, 2), (3, 2), (4, 2), (5, 1), (6, 2), (7, 2), (10, 1)]
        >>> merge([[], []])
        []
        >>> merge([[1], [2], [3]])
        [(1, 1), (2, 1), (3, 1)]
        >>> merge([[1], [2, 4], []])
        [(1, 1), (2, 1), (4, 1)]
        """
    start = time.time()
    record_counter = Counter()
    for l in lists:
        record_counter.update(l)
    duration = (time.time() - start) * 1000
    sys.stderr.write("Merging lists took %.0f ms.\n" % duration)
    return list(record_counter.items())


def compute_ped(prefix, str, delta):
    """ Check wether the prefix edit distance between prefix
        and str is at most delta

        >>> compute_ped("foo", "foo", 0)
        0
        >>> compute_ped("foo", "foo", 10)
        0
        >>> compute_ped("foo", "foot", 10)
        0
        >>> compute_ped("foot", "foo", 1)
        1
        >>> compute_ped("foo", "fotbal", 1)
        1
        >>> compute_ped("foo", "bar", 3)
        3
        >>> compute_ped("perf", "perv", 1)
        1
        >>> compute_ped("perv", "perf", 1)
        1
        >>> compute_ped("perf", "peff", 1)
        1
        >>> compute_ped("foot", "foo", 0)
        1
        >>> compute_ped("foo", "fotbal", 0)
        1
        >>> compute_ped("foo", "bar", 2)
        3
        >>> compute_ped("uniwer", "university", 6)
        1
        >>> compute_ped("munchen", "münchen", 1)
        1
        """
    # Account for epsilon
    n = len(prefix) + 1
    m = min(len(prefix) + delta + 1, len(str) + 1)
    # Initialize matrix
    matrix = [[0 for _ in range(m)] for _ in range(n)]
    for j in range(1, n):
        matrix[j][0] = j
    for j in range(1, m):
        matrix[0][j] = j
    # Dynamic programming.
    for i in range(1, n):
        for j in range(1, m):
            repl = matrix[i - 1][j - 1] + 1
            if prefix[i - 1] == str[j - 1]:
                repl = matrix[i - 1][j - 1]
            matrix[i][j] = min(min(repl, matrix[i][j - 1] + 1),
                               matrix[i - 1][j] + 1)
    ped = min(matrix[n - 1])
    return ped

def levenshtein(seq1, seq2):
    match = 0
    mismatch = 1
    gap_penalty = 1
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + gap_penalty,
                    matrix[x-1, y-1] + match,
                    matrix[x, y-1] + gap_penalty
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + gap_penalty,
                    matrix[x-1,y-1] + mismatch,
                    matrix[x,y-1] + gap_penalty
                )
    return (matrix[size_x - 1, size_y - 1])


def needleman_wunsch_scoring(seq1, seq2):
    match = -1
    mismatch = 1
    gap_penalty = 1
    gap_opening = 3
    gap_opened = False
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + gap_penalty,
                    matrix[x-1, y-1] + match,
                    matrix[x, y-1] + gap_penalty
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + gap_penalty,
                    matrix[x-1,y-1] + mismatch,
                    matrix[x,y-1] + gap_penalty
                )
            if (matrix[x, y] == matrix[x - 1, y] + gap_penalty or matrix[x, y - 1] + gap_penalty) and not gap_opened:
                matrix[x, y] += gap_opening
                gap_opened = True
            else:
                gap_opened = False

    return (matrix[size_x - 1, size_y - 1])

def affine_gap_scoring(seq1, seq2):
    match = -3
    mismatch = 1
    gap_penalty = 0.5
    gap_opening = 3
    gap_opened = False
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + gap_penalty,
                    matrix[x-1, y-1] + match,
                    matrix[x, y-1] + gap_penalty
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + gap_penalty,
                    matrix[x-1,y-1] + mismatch,
                    matrix[x,y-1] + gap_penalty
                )
            if (matrix[x, y] == matrix[x - 1, y] + gap_penalty or matrix[x, y - 1] + gap_penalty):
                if not gap_opened:
                    matrix[x, y] += gap_opening
                    gap_opened = True
            else:
                gap_opened = False
    return (matrix[size_x - 1, size_y - 1])

class QgramIndex:
    """ A q-gram index, adapted from the inverted index code from Lecture 1.

    >>> qi = QgramIndex(3)
    >>> qi.build_from_file("example_solution.txt")
    >>> sorted(qi.inverted_lists.items())
    [('$$f', [0, 1, 2, 3]), ('$fo', [0, 1, 2, 3]), ('all', [0]), \
('arc', [3]), ('bal', [0]), ('bar', [1, 3]), ('foo', [0, 1, 2, 3]), \
('oba', [1]), ('oob', [1]), ('oot', [0, 2, 3]), ('otb', [0, 3]), \
('ots', [2]), ('rca', [3]), ('sal', [2]), ('tba', [0, 3]), ('tsa', [2])]
    """

    def __init__(self, q):
        """ Create an empty q-gram index for given q (size of the q-grams). """
        self.inverted_lists = dict()
        self.q = q
        self.vocab = dict()
        self.coordinates = []
        self.types = []
        self.scoring_method = SCORING_TYPE.AFFINE_GAPS


    def build_from_file(self, file_name):
        """ Build index for text in given file, one record per line. """

        with open(file_name, 'r', encoding='utf-8', errors='replace') as file:
            record_id = 0
            for line in file:
                # If the line starts with a tie-fighter we continue.
                if line.startswith("#::#"):
                    continue
                # split line by tabs.
                splitted = re.split(r'\t+', line)
                # first tab is the city name/record
                record = splitted[0].strip()
                self.vocab[record_id] = record
                # the if/else contructs are necessary because the file lines
                # dont got always 3 entries
                # second tab, coordinates
                if(len(splitted) > 1):
                    self.coordinates.append(splitted[1])
                else:
                    self.coordinates.append(None)

                # second tab, coordinates
                if (len(splitted) > 2):
                    if splitted[2] == 'Arena\n':
                        self.types.append("Arena")
                    elif splitted[2] == 'Pokestop\n':
                        self.types.append("Pokestop")
                    else:
                        self.types.append("Arena/Pokestop")
                else:
                    self.types.append(None)

                # on the fly calc qgrams
                word = re.sub("[ \W+\n]", "", record).lower()
                qgrams = get_qgrams(word, self.q)
                for qgram in qgrams:
                    # print(qgram)
                    if qgram not in self.inverted_lists:
                        self.inverted_lists[qgram] = list()
                    self.inverted_lists[qgram].append(record_id)
                record_id += 1

            for record in file:
                record = record.strip()
                self.vocab[record_id] = record
                word = re.sub("[ \W+\n]", "", record).lower()
                qgrams = get_qgrams(word, self.q)
                for qgram in qgrams:
                    if qgram not in self.inverted_lists:
                        self.inverted_lists[qgram] = list()
                    self.inverted_lists[qgram].append(record_id)
                record_id += 1

    def get_posting_list(self, qgram):
        """ Returns the posting list for the given word if it exists else an
        empty list.

        >>> qi = QgramIndex(3)
        >>> qi.build_from_file("example_solution.txt")
        >>> qi.get_posting_list("foo")
        [0, 1, 2, 3]
        >>> qi.get_posting_list("$$f")
        [0, 1, 2, 3]
        >>> qi.get_posting_list("all")
        [0]
        >>> qi.get_posting_list("tsa")
        [2]
        >>> qi.get_posting_list("ned")
        []
        """
        return self.inverted_lists.get(qgram, [])

    def find_matches(self, query, delta, k=5, use_qindex=True):
        """ Find the top-k matches

        >>> qi = QgramIndex(3)
        >>> qi.build_from_file("example_solution.txt")
        >>> len(qi.find_matches("foo", 0))
        4
        >>> len(qi.find_matches("foos", 1))
        4
        >>> len(qi.find_matches("foos", 0))
        4
        >>> len(qi.find_matches("ball", 1))
        1
        >>> len(qi.find_matches("football", 1))
        4
        >>> len(qi.find_matches("football", 10))
        4
        >>> len(qi.find_matches("kartoffelsalat", 3))
        0
            """
        result_words = []
        # We use the q-gram index to pre-filter.
        if use_qindex:
            qgrams = get_qgrams(query, self.q)
            record_lists = [self.get_posting_list(qgram) for qgram in qgrams]
            merged_lists = merge(record_lists)
            threshold = (len(query) + self.q - 1) / 4
            sys.stderr.write("query %s\n" % (query))
            sys.stderr.write("Threshold %d\n" % (threshold))
            n_ped_computations = 0
            start = time.time()
            for record_id, count in merged_lists:
                record = self.vocab[record_id]
                word = re.sub("[ \W+\n]", "", record).lower()
                sys.stderr.write("Word: %s -- Qgrams in common: %d\n" % (word, count))
                if count >= int(threshold):
                    if self.scoring_method == SCORING_TYPE.LEVENSHTEIN:
                        ed = levenshtein(query, word)
                    elif self.scoring_method == SCORING_TYPE.NEEDLEMAN_WUNSCH:
                        ed = needleman_wunsch_scoring(query, word)
                    elif self.scoring_method == SCORING_TYPE.AFFINE_GAPS:
                        ed = affine_gap_scoring(query, word)
                    else:
                        ed = levenshtein(query, word)
                    n_ped_computations += 1
                    coordinates = self.coordinates[record_id]
                    type = self.types[record_id]
                    result_words.append((record, coordinates, type, ed))
            duration = (time.time() - start) * 1000
            sys.stderr.write("Computing ED for %s words took %.0f ms.\n" %
                         (n_ped_computations, duration))
        result = sorted(result_words, key=lambda x: x[3], reverse=False)[:k]
        return result
