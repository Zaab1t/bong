__all__ = ['mdb_entry_maker']


def document(doc_type, document_data, **kwargs):
    doc = doc_type()
    doc(document_data, **kwargs)
    return doc
