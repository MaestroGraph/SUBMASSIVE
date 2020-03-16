# SUBMASSIVE
# Shuai Wang
# shuai.wang@vu.nl
# All rights reserved.
# === 
# this in this file we obtain all the subClassOf statements and try to see how to
# resolve the cycles

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
sys.setrecursionlimit(10000)
PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
PATH_SAMEAS_NETWORK = "/home/jraad/ssd/data/identity-data/"
PATH_ID2TERMS_099 = "/home/jraad/ssd/data/identity-data-0_99/id2terms_0-99.csv"
PATH_TERM2ID_099 = "/home/jraad/ssd/data/identity-data-0_99/term2id_0-99.csv"

hdt_lod = HDTDocument(PATH_LOD)

id_type = hdt_lod.convert_term("http://www.w3.org/1999/02/22-rdf-syntax-ns#type", IdentifierPosition.Predicate)
id_sameAs = hdt_lod.convert_term("http://www.w3.org/2002/07/owl#sameAs", IdentifierPosition.Predicate)
id_subClassOf = hdt_lod.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
id_equivalentClass = hdt_lod.convert_term("http://www.w3.org/2002/07/owl#equivalentClass", IdentifierPosition.Predicate)



# Quesiton 1: set things up
start = time.time()
l = []

(subclasstriples, cardinality) = hdt_lod.search_triples("", "http://www.w3.org/2000/01/rdf-schema#subClassOf", "")
for (s, p, o) in subclasstriples:
    l.append((s, o))


# then convert to a directed network
print ('list size: ', len(l))

TOTAL = 4461717
TOTAL_split = 10000 # originall it was 100000

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

l_split = list(split(l, TOTAL_split))
print ('total segment size = ', len(l_split))

# l = l[ (int)(53750*TOTAL/TOTAL_split):]
# 4,461,717


for i in range(len(l_split)):
    ll = l_split[i]
    g = nx.DiGraph(ll)
    # print(list(nx.simple_cycles(g)))
    all_cycles = list(nx.simple_cycles(g))


    if len(all_cycles) > 0:
        with open('data3/cycles'+ str(i) +'.json', 'w') as json_file:
            json.dump(all_cycles, json_file)
        # print ('print cycles ==== ')
            # for c in all_cycles:
            #     # print (c, '\n')
            #     json.dump(c, json_file)
        # print ('total split =', TOTAL_split,' each of size ', TOTAL/TOTAL_split)
        print(' we are dealing with ', i)
        # print ('length = ' , len(all_cycles))
    i += 1
    print (i)

# print (nx.cycle_basis(g.to_undirected()))

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Q10: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
#
