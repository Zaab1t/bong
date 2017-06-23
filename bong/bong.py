"""
    bong.py
    ~~~~~~~

    Search engine in Python.
"""


__all__ = [
    'terms_in_document',
    'DocumentVector',
    'dot_product',
    'cosine_similarity',
    'vector_space_search',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


from collections import Counter
from math import sqrt


def terms_in_document(document):
    """Return the terms in *document*.

    :rtype: generator of strs.
    """
    return document.split()


class DocumentVector(Counter):
    """Represent a document as a vector.

    Subclass of :class:'collections.Counter'.
    """

    def __init__(self, document):
        super().__init__(terms_in_document(document))
        self.document = document

    @property
    def magnitude(self):
        """Return the magnitude of vector.

        https://en.wikipedia.org/wiki/Magnitude_(mathematics)

        :rtype: float.
        """
        return sqrt(sum(i**2 for i in self.values()))


def dot_product(v1, v2):
    """Return the dot product of two vectors.

    https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition

    :rtype: int.
    """
    return sum(count*v2[term] for term, count in v1.items())


def cosine_similarity(v1, v2):
    """Return the cosine similarity of two vectors.

    https://en.wikipedia.org/wiki/Cosine_similarity

    :rtype: float.
    """
    return dot_product(v1, v2) / (v1.magnitude * v2.magnitude)


def vector_space_search(query, *documents):
    """Return (vector of document, score) for *documents*.

    The score is the cosine similarity between the query and the document.
    The closer score is to 1, the better the result is. 0 means zero
    overlap in terms of terms :)

    http://ondoc.logand.com/d/2697/pdf

    :param query: str.
    :param documents: iterable of strs.
    :rtype: generator, yields (vector, cosign)
    """
    vectors = [DocumentVector(document) for document in documents]
    query_vector = DocumentVector(query)
    for vector in vectors:
        yield vector, cosine_similarity(query_vector, vector)


if __name__ == '__main__':
    d1 = 'cat mouse mouse cat dog mouse cat mouse'
    d2 = 'dog cat dog mouse mouse mouse mouse mouse'
    d3 = 'dog cat dog cat dog'
    for vector, result in vector_space_search('mouse', d1, d2, d3):
        print(vector, ':', result)
