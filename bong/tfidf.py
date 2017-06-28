"""
    tfidf.py
    ~~~~~~~~

    Term frequency-inverse document frequency.

    https://en.wikipedia.org/wiki/Tf%E2%80%93idf
"""


__all__ = [
    'term_frequency',
    'inverse_document_frequency',
    'tfidf',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from pymongo import MongoClient
from functools import lru_cache
from math import log


client = MongoClient()
db = client['bong']
documents = db['documents']
terms = db['tfidf']


@lru_cache()
def _get_term(term):
    return terms.find_one({'term': term})


def term_frequency(term, doc):
    """Return the augmented term frequency of *term*.

    We use augmented term frequency to prevent bias towards longer
    documents.

    https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2
    """
    tf = _get_term['frequency']
    max_tf_in_doc = max(doc['token_counter'].values())
    return 0.5 + 0.5 * tf/max_tf_in_doc


def inverse_document_frequency(term):
    """Return the inverse document frequency of *term*.

    This is a measure of how much information *term* provides.

    https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
    """
    N = documents.count()
    term_refs = _get_term(term)['references']
    return log(N / (1 + term_refs))


def tfidf(term, doc):
    """Return the term frequency-inverse document frequency of *term*.

    tf-idf is a number between 0 and 1 that reflects how important
    *term* is in the context of *doc*.

    https://en.wikipedia.org/wiki/Tf%E2%80%93idf
    """
    return term_frequency(term, doc) * inverse_document_frequency(term)


def adjust_with_counter(counter):
    """Add term frequencies of *counter* to db."""
    for term, frequency in counter.items():
        entry = _get_term(term)
        if not entry:
            entry = {
                'term': term,
                'frequency': frequency,
                'references': 1,
            }
            terms.insert_one(entry)
            continue
        entry['frequency'] += frequency
        entry['references'] += 1
        terms.update_one({'_id': entry['_id']}, entry)
