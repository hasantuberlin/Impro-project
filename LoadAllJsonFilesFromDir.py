'''
loading data in elasticsearch
'''

import requests, json, os
from elasticsearch import Elasticsearch


#connecting to elastic search


res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        f = open(filename)
        print(filename)
        #docket_content = f.read()
        # Send the data into es
        #es.index(index='myindex', ignore=400, doc_type='docket', 
        #id=i, body=json.loads(docket_content))
        #i = i + 1