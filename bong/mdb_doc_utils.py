__all__ = ['mdb_entry_maker']


def mdb_entry_maker(doc_type, document, **kwargs):
    doc = doc_type()
    doc(document, **kwargs)
    return doc
