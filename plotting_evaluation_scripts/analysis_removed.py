# analysis removed cycles

from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
# import rocksdb
import codecs
import datetime
import pickle
import time
import networkx as nx
import sys
import csv
from collections import Counter
import tldextract

DOMAIN = 'carleton'

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"

hdt_file = HDTDocument(PATH_LOD)

def print_info(sbj, obj):
    predicate_names = [
    "http://sw.cyc.com/CycAnnotations_v1#label",
    "http://www.w3.org/2000/01/rdf-schema#comment",
    "http://www.w3.org/2000/01/rdf-schema#label"
    ]

    s_domain = tldextract.extract(sbj).domain
    o_domain = tldextract.extract(obj).domain
    # filter that domain
    if (s_domain != DOMAIN and o_domain != DOMAIN):
        # print (DOMAIN)
        print ('SUBJECT: ', sbj)
        for p in predicate_names:
            (triples, cardinality) = hdt_file.search_triples(sbj, p, "")
            for (s, p, o) in triples:
                print ('\tPREDICATE: ', p)
                print ('\t\t Comments/labels  :', o,'\n')
        print ('OBJECT: ', obj)
        for p in predicate_names:
            (triples, cardinality) = hdt_file.search_triples(obj, p, "")
            for (s, p, o) in triples:
                print ('\tPREDICATE: ', p)
                print ('\t\t Comments/labels  :', o,'\n')

        print ('\n\n========================\n\n')


eq_file = open('final_removed_edges60.csv', 'r', newline='')
reader = csv.DictReader(eq_file)
pair = []
for row in reader:
    s_id = row["SUBJECT_ID"]
    s = row["SUBJECT"]
    o_id = row["OBJECT_ID"]
    o = row["OBJECT"]
    pair.append((s, s_id, o, o_id))

# Analysis of Opencyc cycles
# for (s, o) in pair:
#     print_info(s, o)
#     s_domain = tldextract.extract(s).domain
#     o_domain = tldextract.extract(o).domain
#     if (s_domain == 'opencyc' and o_domain == DOMAIN):
#         p = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
#         (triples, cardinality) = hdt_file.search_triples(o, p, s)
#         if cardinality != 0:
#             print ('there is a reverse in hdt:', triples)
#         if (o, s) in pair:
#             print ('the reverse has also been removed')
#         # input()

man_file = open('lod-two-cycle.csv', 'r')
man_reader = csv.DictReader(man_file)
man_pair = []
for row in man_reader:
    s_id = int(row["SUBJECT_ID"])
    s = row["SUBJECT"]
    o_id = int(row["OBJECT_ID"])
    o = row["OBJECT"]
    sug = row["SUGGESTION"]
    if sug == 'unknown':
        man_pair.append((s, o))


count_man_unknown = 0

for (s, s_id, o, o_id) in pair:
    if (s, o) in man_pair:
        count_man_unknown += 1
    else:
        print_info(s, o)


print ('also appear in the manual decison as unknown: ', count_man_unknown)
