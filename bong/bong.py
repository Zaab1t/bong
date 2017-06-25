"""
    bong.py
    ~~~~~~~

    The main algorithm used for searching.
"""


__all__ = ['search']
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


def search(query, n):
    """Search for *query* and return the *n* most relevant results.

    It is important that *query* is a subclass of
    :class:'bong.BaseDocument'.
    """
