"""
    docprocessing.py
    ~~~~~~~~~~~~~~~~

    Provide the tools to prepare a given document for comparisons.

    This module exposes the following functions:
        * tokenize -- split a document into its' terms.
        * stem_words -- strip word suffixes.
        * remove_stop_words -- remove common words of no semantic value.
"""


__all__ = [
    'tokenize',
    'stem_words',
    'remove_stop_words',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from Stemmer import Stemmer
import stop_words as stopwords
from functools import lrucache


def tokenize(document):
    """Return all the terms in *document*."""
    return document.split()


def stem_words(iterable, language='english'):
    """Stem every word in iterable.

    Uses PyStemmer which is based on the Porter Stemming algorithms -
    an algorithm for suffix stripping.

    https://tartarus.org/martin/PorterStemmer/def.txt

    :rtype: list.
    """
    try:
        stemmer = Stemmer(language)
    except KeyError:
        stemmer = Stemmer('english')
    return stemmer.stemWords(iterable)


@lru_cache(maxsize=len(stopwords.AVAILABLE_LANGUAGES))
def _get_stop_words(language):
    """Return stemmed stop words for *language*."""
    stop_words = stopwords.get_stop_words(language)
    return set(stem_words(stop_words, language))


def remove_stop_words(iterable, language='english'):
    """Remove all stop words in *iterable*.

    Stop words are common words which add no semantic value to a sentence.

    :rtype: generator.
    """
    stop_words = _get_stop_words(language)
    for word in iterable:
        if word not in stop_words:
            yield word
