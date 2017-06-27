'''
Document types!
'''

from abc import ABCMeta, abstractmethod

from collections import Counter
from string import whitespace, punctuation

from bs4 import BeautifulSoup as bs


__all__ = ['BaseDocument', 'Query', 'HtmlDocument']


class BaseDocument(metaclass=ABCMeta):
    '''Base document type for preparing documents to be stored
       in the database.

       Subclasses must implement .tokenize such that the subclass'
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
    def tokenize(self):
        '''Implement me!'''


class HtmlDocument(BaseDocument):
    '''The html document type for preparing html documents
    for storage in mongodb.
    '''
    _PUNCTUATION = punctuation.replace("'", '')
    _PUNCTUATION = _PUNCTUATION.replace("&", '')
    _WHITESPACE = whitespace.replace(' ', '')
    _BANNED_CHARS = _WHITESPACE + _PUNCTUATION

    def tokenize(self, document_data, tag_ranking=None):
        '''Accepts html in any format bs4 can soupify.
        May be initialised with biasd html tag rankings to
        influence searches.

        :rtype: HtmlDocument
        '''
        soup, all_text = self.simplify_html_data(document_data)
        zones = dict()
        all_text = Counter(all_text.split(' '))
        del all_text['']
        self.token_counter = dict(all_text)
        return self

    def simplify_html_data(self, document_data):
        '''Lowercases the file and removes chars *generally*
        not associated with normal phrasing.

        :rtype: bs4 soup object, str
        '''
        document_data = document_data.lower()
        soup = bs(document_data, 'html.parser')
        all_text = list(soup.text)
        for i, char in enumerate(all_text):
            if char in self._BANNED_CHARS:
                all_text[i] = ' '
        all_text = ''.join(all_text)
        return soup, all_text


class Query(BaseDocument):
    def tokenize(self, document_data, tag_ranking=None):
        self.token_counter = dict(Counter(document_data.split()))
        return self
