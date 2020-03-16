

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
PATH_DBpedia = "/Users/sw-works/Documents/New_start/dbpedia2016April/dbpedia2016-04en.hdt"



def generate_reduced():
    # Q1 : retrieve the subClassOf relations
    hdt_file = None
    output_filename = None
    output_selfloopClass_filename = None
    output_leafClass_filename = None
    output_intermediateClass_filename = None

    if sys.argv [1] == 'lod':
        hdt_file = HDTDocument(PATH_LOD)
        output_filename = 'reduced_lod_subClassOf.csv'
        output_selfloopClass_filename = 'lod_selfloop_classes.csv'
        output_leafClass_filename = 'lod_leaf_classes.csv'
        output_intermediateClass_filename = 'further_reduced_lod_subClassOf.csv'
    else:
        hdt_file = HDTDocument(PATH_DBpedia)
        output_filename = 'dbpedia_subClassOf.csv'
        output_selfloopClass_filename = 'dbpedia_selfloop_classes.csv'
        output_leafClass_filename = 'dbpedia_leaf_classes.csv'
        output_intermediateClass_filename = 'further_reduced_dbpedia_subClassOf.csv'

    subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    id_subClassOf = hdt_file.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)

    (subclass_triples, cardinality) = hdt_file.search_triples("", subClassOf, "")

    c1 = ['196338233', '196338418', '196338419']
    c2 = ['196338233', '196338325', '196338412']
    c3 = ['196337995', '196338014', '196338013']
    c4 = ['196338014', '196338063', '196338410']

    cs = [c1, c2, c3, c4]
    for c in cs:
        print ('\n\n this cycle = ', c)
        for n in c:
            print ('id =', n)
            name = hdt_file.convert_id(int(n), IdentifierPosition.Subject)
            print ('name = ', name)
            s_id = hdt_file.convert_term(name, IdentifierPosition.Subject)
            print ('when its subject = ', s_id)
            o_id = hdt_file.convert_term(name, IdentifierPosition.Object)
            print ('when its object  = ', o_id)

    print ('==================================')

    c1 = ['1193056652', '1193056593', '1193056657']
    c2 = ['1146303708', '1146299369', '1146331327']
    c3 = ['196338400', '196338312', '196338288']
    c4 = ['196338013', '196337995', '196338014']
    c5 = ['196338242', '196338410', '196337957']
    c6 = ['196338418', '196338419', '196338233']
    c7 = ['196338233', '196338325', '196338412']
    c8 = ['196338014', '196338063', '196338410']
    c9 = ['196338014', '196337975', '196338007']
    c10 =['196338050', '196338049', '196337975']
    c11 = ['196338197', '196338462', '196338406']
    c12 = ['196338220', '196338217', '196338034']
    c13 = ['196338145', '196338152', '196338419']
    c14 = ['196338288', '196338116', '196337978']
    c15 = ['196338070', '196338360', '196338241']
    c16 = ['114657709', '114657713', '125181834']

    cs = [c1, c2, c3, c4, c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16]
    for c in cs:
        print ('\n\n that cycle = ', c)
        for n in c:
            print ('id =', n)
            name = hdt_file.convert_id(int(n), IdentifierPosition.Subject)
            print ('name = ', name)
            s_id = hdt_file.convert_term(name, IdentifierPosition.Subject)
            print ('when its subject = ', s_id)
            o_id = hdt_file.convert_term(name, IdentifierPosition.Object)
            print ('when its object  = ', o_id)

if __name__ == "__main__":
#    generate()
#    load()
    generate_reduced()
