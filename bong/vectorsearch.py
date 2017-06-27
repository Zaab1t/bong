"""
    vectorsearch.py
    ~~~~~~~~~~~~~~~

    Implements the functionality to compare documents as if they were
    vectors. More specifically it implements the vector space model.
"""


__all__ = [
    'magnitude',
    'dot_product',
    'cosine_similarity',
    'vector_space_search',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from math import sqrt


def magnitude(document):
    """Return the magnitude of *document*.

    https://en.wikipedia.org/wiki/Magnitude_(mathematics)

    :rtype: float.
    """
    return sqrt(sum(i**2 for i in document['token_counter'].values()))


def dot_product(doc1, doc2):
    """Return the dot product of two documents.

    https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition

    :rtype: int.
    """
    v1 = doc1['token_counter']
    v2 = doc2['token_counter']
    return sum(count*v2.get(term, 0) for term, count in v1.items())


def cosine_similarity(doc1, doc2):
    """Return the cosine similarity of two documents.

    https://en.wikipedia.org/wiki/Cosine_similarity

    :rtype: float.
    """
    return dot_product(doc1, doc2) / (magnitude(doc1) * magnitude(doc2))


def vector_space_search(query, *documents):
    """Return (document, score) for each document in *documents*.

    The score is the cosine similarity between the query and the document.
    The closer score is to 1, the better the result is. 0 means zero
    overlap in terms of terms :)

    http://ondoc.logand.com/d/2697/pdf

    :param query: document.
    :param documents: iterable of documents.
    :rtype: generator, yields (doc, similarity)
    """
    for doc in documents:
        yield doc, cosine_similarity(query, doc)
