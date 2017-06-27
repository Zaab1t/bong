from pymongo import MongoClient
from pprint import pprint
import requests

from bong import search, document, HtmlDocument, Query


sample_urls = [
    'https://theelous3.net/CamelCase',
    'https://theelous3.net/concurrency_primer',
    'https://theelous3.net/anti_patterns',
]


def fill_collection(collection):
    documents = []
    for url in sample_urls:
        r = requests.get(url)
        doc = document(HtmlDocument, r.content).as_db_entry()
        documents.append(doc)
    collection.insert_many(documents)


if __name__ == '__main__':
    client = MongoClient()
    db = client['bong']
    collection = db['documents']
    entries = collection.count()
    print('Collection has', entries, 'entries.')
    if entries == 0:
        fill_collection(collection)
    for data in iter(input, 'quit'):
         query = document(Query, data)
         for result in search(query.as_db_entry(), 2):
             pprint(result)
    print('bye')
