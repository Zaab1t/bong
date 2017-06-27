"""
    bong.py
    ~~~~~~~

    The main algorithm used for searching.
"""


__all__ = ['search']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from pymongo import MongoClient

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
    def key(x): return x[1]
    for doc, _ in sorted(result, key=key, reverse=True)[:n]:
        yield doc
