
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
    pattern  = re.compile(r'(„|“|\'|„|“|”|‘|’)')
    string = pattern.sub('"', string)
    return string
