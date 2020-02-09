
'''
loading data in elastic search
'''

import requests, json, os
from elasticsearch import Elasticsearch
import pprint
import re
import json
from datetime import datetime
import sys



#directory = '/Desktop/impro project/test'

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])



with open('s02280.json') as json_file:
    listOfJson = json.load(json_file)
    #print(type(data))

    for jsonDoc in listOfJson: 
    	es.index(index = 'imrprowithmap', body= jsonDoc)

