from collections import Counter
from string import whitespace, punctuation

from bs4 import BeautifulSoup as bs

__all__ = ['mdb_entry_maker']

# this is pretty rough ofc
_PUNCTUATION = PUNCTUATION.replace("'", '')
_PUNCTUATION = PUNCTUATION.replace("&", '')
_WHITESPACE = WHITESPACE.replace(' ', '')
_BANNED_CHARS = _WHITESPACE + _PUNCTUATION


def _itemise_html(document):
    document = document.lower()
    soup = bs(document, 'html.parser')
    all_text = list(soup.text)
    for i, char in enumerate(all_text):
        if char in _BANNED_CHARS:
            all_text[i] = ' '
    all_text = ''.join(all_text)
    page = dict()
    for x in soup.find_all():
        if x.string:
            try:
                page[x.name].update(x.string.split())
            except KeyError:
                page[x.name] = set(x.string.split())
    all_text = Counter(all_text.split(' '))
    del all_text['']
    return page, all_text


def mdb_entry_maker(doc_type, document, index_ranking=None):
    itemised_doc, doc_all_tokens = _itemise_html(document)
    if index_ranking:
        zone_weights = {k: index_ranking.setdefault(k, 0)
                        for k in itemised_doc}
    else:
        zone_weights = {k: 0 for k in itemised_doc}
    return doc_type(zone_weights, itemised_doc, doc_all_tokens)
