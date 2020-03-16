# integrate
from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
# import rocksdb
import codecs
import datetime
import pickle
import time
import json
import networkx as nx

import sys
import subprocess

# collect all the names about json

TOTAL_split = 10000
data_collection = []
for i in range (TOTAL_split):
    fname = './data3/cycles' + str(i) + '.json'
    try:
        with open(fname) as f:
            data = json.load(f)
            data_collection += list(data)
            # for d in data:
            #     print (d)
    except:
        pass



with open('data3/all_cycles.json', 'w') as json_file:
    json.dump(data_collection, json_file)

with open('data3/all_cycles.json') as f:
    data = json.load(f)
    print ('total entries = ', len(data))
    # if ['http://crm.rkbexplorer.com/id/E5.Event'] in data :
    #     print ('found')
    # for d in data [0:20]:
    #     print (d)
