"""
    bong.py
    ~~~~~~~

    The main algorithm used for searching.
"""


__all__ = ['search']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from pymongo import MongoClient
from itertools import islice

from .vectorsearch import vector_space_search


def search(query, n):
    """Search for *query* and return the *n* most relevant results.

    It is important that *query* is a subclass of
    :class:'bong.BaseDocument'.
    """
    client = MongoClient()
    db = client['bong']
    collection = db['documents']
    result = vector_space_search(query, *collection.find())
    k = lambda x: x[1]
    for doc, similarity in islice(reversed(sorted(result, key=k)), n):
        yield doc
