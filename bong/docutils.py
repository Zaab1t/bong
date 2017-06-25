__all__ = ['mdb_entry_maker']


def document(doc_type, document_data, **kwargs):
    '''Create abitrary documents of `doc_type`.

    :rtype: doc_type
    '''
    doc = doc_type()
    doc(document_data, **kwargs)
    return doc
