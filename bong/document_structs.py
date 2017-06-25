'''
Document types!
'''

from collections.abc import Mapping

__all__ = ['HtmlDocument']


class DocumentBase:
    def __init__(self, zone_weights, zones, token_counter):
        self.zone_weights = zone_weights
        self.zones = zones
        self.token_counter = token_counter

    def __contains__(self, x):
        return x in self.token_counter

    def as_db_entry(self):
        return self.__dict__

    def modify_ranking(self, new_ranks):
        self.zone_weights.update(new_ranks)


class HtmlDocument(DocumentBase):
    def __init__(self, *args, metadata=None):
        if metadata:
            assert isinstance(metadata, Mapping)
            self.metadata = metadata
        super().__init__(*args)
