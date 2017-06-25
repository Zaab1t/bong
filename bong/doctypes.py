'''
Document types!
'''

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
    '''Base document type for preparing documents to be stored
       in the database.

       Subclasses must implement __call__ such that the subclass'
       .__dict__ is appropriate for storage in mongodb.
    '''
    def __init__(self):
        self.zone_weights = None
        self.zones = None
        self.token_counter = None

    def __contains__(self, x):
        return x in self.token_counter

    def as_db_entry(self):
        return self.__dict__

    def modify_ranking(self, new_ranks):
        '''Alter the weights of zone types for consideration
        during vector search.
        '''
        self.zone_weights.update(new_ranks)

    @abstractmethod
    def __call__(self):
        '''Implement me!'''


class HtmlDocument(BaseDocument):
    '''The html document type for preparing html documents
    for storage in mongodb.
    '''
    def __call__(self, document, tag_ranking=None):
        '''Accepts html in any format bs4 can soupify.
        May be initialised with biasd html tag rankings to
        influence searches.

        :rtype: HtmlDocument
        '''
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
