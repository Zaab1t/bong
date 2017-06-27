"""
    terminfrequency.py
    ~~~~~~~~~~~~~~~~~~

    Works much like a dictionary, in the sense that it maps a given
    term to its' frequency (the number of times it has appeared).
"""

__all__ = [
    'get',
    'increment',
    'increment_with_counter',
    'save_json',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import json


try:
    with open('terminfrequency.json', encoding='utf-8') as f:
        term_mapping = json.loads(f.read())
except FileNotFoundError:
    term_mapping = {}


def get(term):
    """Return the number of times *term* has appeared."""
    return term_mapping.get(term, 0)


def increment(term, i=1):
    """Increment the times term has appeared."""
    try:
        term_mapping[term] += i
    except KeyError:
        term_mapping[term] = 1


def increment_with_counter(counter):
    """Increment the times term has appeared by the frequency in
    *counter*.
    """
    for term, frequency in counter.items():
        try:
            term_mapping[term] += frequency
        except KeyError:
            term_mapping[term] = frequency


def save_json():
    """Save the <term, frequency> mapping to a file."""
    with open('terminfrequency.json', 'w') as f:
        f.write(json.dumps(term_mapping))
