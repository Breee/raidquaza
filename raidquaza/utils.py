from collections import Counter  # Counter counts the number of occurrences of each item
from itertools import tee, count
import re


def replace_quotes(string):
    """
    >>> test_string =  '„Kyogre HBF Freiburg“'
    >>> replace_quotes(test_string)
    '"Kyogre HBF Freiburg"'

    >>> test_string =  '“Kyogre HBF Freiburg“'
    >>> replace_quotes(test_string)
    '"Kyogre HBF Freiburg"'

    >>> test_string =  '”Kyogre HBF Freiburg”'
    >>> replace_quotes(test_string)
    '"Kyogre HBF Freiburg"'

    """
    # replace („|“|\'|„|“|”|‘|’) with "
    pattern = re.compile(r'(„|“|\'|„|“|”|‘|’)')
    string = pattern.sub('"', string)
    return string


def uniquify(seq):
    dups = {}
    for i, val in enumerate(seq):
        if val not in dups:
            # Store index of first occurrence and occurrence value
            dups[val] = [i, 1]
        else:
            # Special case for first occurrence
            if dups[val][1] == 1:
                seq[dups[val][0]] += str(dups[val][1])

            # Increment occurrence value, index value doesn't matter anymore
            dups[val][1] += 1

            # Use stored occurrence value
            seq[i] += str(dups[val][1])
    return seq
