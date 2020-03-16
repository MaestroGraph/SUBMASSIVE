# this script is to test the id of a URI is the same.

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

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_file = HDTDocument(PATH_LOD)
# (triples, cardinality) = hdt_file.search_triples("", "", "")
(triples, cardinality) = hdt_file.search_triples("", "http://www.w3.org/2000/01/rdf-schema#subClassOf", "")
flag = False

zeros = []

for (s, p, o) in triples:
    # get the id of s at subject and object
    id_s_subject = hdt_file.convert_term(s, IdentifierPosition.Subject)
    id_s_object = hdt_file.convert_term(s, IdentifierPosition.Object)
    if (id_s_subject != id_s_object):
        flag = True
        print ('ERROR as subject', s, id_s_subject, id_s_object)
        # (triples, cardinality) = hdt_file.search_triples(s, "http://www.w3.org/2000/01/rdf-schema#subClassOf", "")
        # print ('when as subject', cardinality)
        # (triples, cardinality) = hdt_file.search_triples("", "http://www.w3.org/2000/01/rdf-schema#subClassOf", s)
        # print ('when as object', cardinality)
        # break
    # same for object
    id_o_subject = hdt_file.convert_term(o, IdentifierPosition.Subject)
    id_o_object = hdt_file.convert_term(o, IdentifierPosition.Object)
    if (id_o_subject != id_o_object):
        flag = True
        print ('ERROR as object', o, id_o_subject, id_o_object)
        # (triples, cardinality) = hdt_file.search_triples(s, "http://www.w3.org/2000/01/rdf-schema#subClassOf", "")
        # print ('when as subject', cardinality)
        # (triples, cardinality) = hdt_file.search_triples("", "http://www.w3.org/2000/01/rdf-schema#subClassOf", s)
        # print ('when as object', cardinality)
        # break
