__all__ = ['document']


def document(document_type, document_data, **kwargs):
    '''Create abitrary documents of `doc_type`.

    :rtype: doc_type
    '''
    doc = document_type().tokenize(document_data, **kwargs)
    return doc
