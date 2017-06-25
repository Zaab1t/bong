'''
Document types!
'''

from collections.abc import Mapping
from abc import ABCMeta, abstractmethod

from collections import Counter
from string import whitespace, punctuation

from bs4 import BeautifulSoup as bs


__all__ = ['HtmlDocument']


_PUNCTUATION = punctuation.replace("'", '')
_PUNCTUATION = _PUNCTUATION.replace("&", '')
_WHITESPACE = whitespace.replace(' ', '')
_BANNED_CHARS = _WHITESPACE + _PUNCTUATION


class BaseDocument(metaclass=ABCMeta):
    def __init__(self, zone_weights=None, zones=None, token_counter=None):
        self.zone_weights = zone_weights
        self.zones = zones
        self.token_counter = token_counter

    def __contains__(self, x):
        return x in self.token_counter

    def as_db_entry(self):
        return self.__dict__

    def modify_ranking(self, new_ranks):
        self.zone_weights.update(new_ranks)

    @abstractmethod
    def __call__(self):
        '''Implement me!'''


class HtmlDocument(BaseDocument):

    def __call__(self, document, tag_ranking=None):
        document = document.lower()
        soup = bs(document, 'html.parser')
        all_text = list(soup.text)
        for i, char in enumerate(all_text):
            if char in _BANNED_CHARS:
                all_text[i] = ' '
        all_text = ''.join(all_text)
        zones = dict()
        for x in soup.find_all():
            if x.string:
                try:
                    zones[x.name].update(x.string.split())
                except KeyError:
                    zones[x.name] = set(x.string.split())
        all_text = Counter(all_text.split(' '))
        del all_text['']
        if tag_ranking:
            zone_weights = {k: tag_ranking.setdefault(k, 0)
                            for k in zones}
        else:
            zone_weights = {k: 0 for k in zones}
        self.zone_weights = zone_weights
        self.zones = zones
        self.token_counter = all_text
        return self
