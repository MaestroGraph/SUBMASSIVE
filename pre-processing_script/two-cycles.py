# SUBMASSIVE
# Shuai Wang
# shuai.wang@vu.nl
# All rights reserved.
# ================================================================
# This file does the following things:
# 1) retrieve the subClassOf relation in csv file (from LOD-a-lot)
# 2) filter out the cycles of size two mannually
# 3) finally, export to a csv file

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

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
# PATH_DBpedia = "/Users/sw-works/Documents/New_start/dbpedia2016April/dbpedia2016-04en.hdt"


def print_ino(n, hdt_file):
    predicate_names = [
    "http://sw.cyc.com/CycAnnotations_v1#label",
    "http://www.w3.org/2000/01/rdf-schema#comment",
    "http://www.w3.org/2000/01/rdf-schema#label"
    ]

    print ('SUBJECT: ', n)
    for p in predicate_names:
        print ('\tPREDICATE: ', p)
        (triples, cardinality) = hdt_file.search_triples(n, p, "")
        for (s, p, o) in triples:
            print ('\t\tOBJECT  :', o,'\n')
    (triples, cardinality) = hdt_file.search_triples(n, "", "")
    print('\t ... other...')
    count = 0
    for (s,p,o) in triples:
        count+=1
        print ('\tPREDICATE: ', p)
        print ('\tOBJECT   : ', o)
        if count >3:
            break
    print ('\n\n')



def generate():
    # Q1 : retrieve the subClassOf relations
    visited_pair_list = []
    # hdt_file = None
    # output_filename = None
    # if sys.argv [1] == 'lod':
    hdt_file = HDTDocument(PATH_LOD)
    output_filename = 'lod-two-cycle.csv'


    subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    id_subClassOf = hdt_file.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
    count = 0
    count_removed = 0
    count_sameas = 0
    count_left = 0
    count_right = 0
    count_sameas = 0
    count_unknown = 0

    cnt_removed = Counter()
    cnt_sameas = Counter()
    cnt_left = Counter()
    cnt_right = Counter()
    cnt_both = Counter()
    cnt_sameas = Counter()
    cnt_unknown = Counter()

    eq_pair_ids = []
    eq_pair_terms = []

    eq_file = open('equivalent-unnecessary-relations.csv', 'r')
    reader = csv.DictReader(eq_file)
    for row in reader:
        s_id = row["SUBJECT_ID"]
        s = row["SUBJECT"]
        o_id = row["OBJECT_ID"]
        o = row["OBJECT"]
        eq_pair_ids.append((s_id, o_id))
        eq_pair_terms.append((s, o))

    with open(output_filename, 'w', newline='') as file:
        (subclass_triples, cardinality) = hdt_file.search_triples("", subClassOf, "")
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT", "SUGGESTION", "DECISION"])

        for (s, p, o) in subclass_triples:
            s_id = hdt_file.convert_term(s, IdentifierPosition.Subject)
            o_id = hdt_file.convert_term(o, IdentifierPosition.Object)
            if s != o :
                # otherwise, it is a self-loop

                # store it in a csv file
                (reverse_subclass_triples, reverse_cardinality) = hdt_file.search_triples(o, subClassOf, s)
                if reverse_cardinality == 1: # there is a reverse link back

                    if (s_id, o_id) in eq_pair_ids or (o_id, s_id) in eq_pair_ids:
                        print ('this is in the equivalence pair, skip it')
                        print (s, '\n', o,'\n\n\n')
                        # Additional: we also make sure it does not appear in the equivalent set
                    else:


                        if (s, o) not in visited_pair_list and (o, s) not in visited_pair_list:
                            # ask the user to deal with it:
                            print ('sbj=\t', s)
                            print ('obj=\t', o)
                            s_domain = tldextract.extract(s).domain
                            o_domain = tldextract.extract(o).domain
                            print ('s_domain = ', s_domain)
                            print ('o_domain = ', o_domain)
                            print_ino(s, hdt_file)
                            print_ino(o, hdt_file)
                            decision = input()
                            count += 1



                            if decision == 'x': # if the entry is meaningless, then remove:
                                writer.writerow([s_id, s, o_id, o, 'remove', 'x'])
                                writer.writerow([o_id, o, s_id, s, 'remove', 'x'])
                                count_removed += 1
                                cnt_removed[s_domain] += 1
                                cnt_removed[o_domain] += 1
                            elif decision == 'l':
                                writer.writerow([s_id, s, o_id, o, 'remove', 'l'])
                                writer.writerow([o_id, o, s_id, s, 'remain', 'l'])
                                count_left += 1
                                cnt_left[s_domain] += 1
                                cnt_left[o_domain] += 1
                                cnt_both[s_domain] += 1
                                cnt_both[o_domain] += 1
                            elif decision == 'r':
                                writer.writerow([s_id, s, o_id, o, 'remain', 'r'])
                                writer.writerow([o_id, o, s_id, s, 'remove', 'r']) # reverse the order
                                count_right += 1
                                cnt_right[s_domain] += 1
                                cnt_right[o_domain] += 1
                                cnt_both[s_domain] += 1
                                cnt_both[o_domain] += 1
                            elif decision == 'e' or decision =='s': # equivalent class. remove both of them
                                writer.writerow([s_id, s, o_id, o, 'remove', 'e'])
                                writer.writerow([o_id, o, s_id, s, 'remove', 'e'])
                                count_sameas += 1
                                cnt_sameas[s_domain] += 1
                                cnt_sameas[o_domain] += 1
                            elif decision == 'u': # unknown, remains to be dealt with automatic approach
                                # count_unknown
                                writer.writerow([s_id, s, o_id, o, 'unknown', 'u'])
                                writer.writerow([o_id, o, s_id, s, 'unknown', 'u'])
                                count_unknown += 1
                                cnt_unknown[s_domain] += 1
                                cnt_unknown[o_domain] += 1
                            else:
                                print ('user input error')

                        visited_pair_list.append( (s, o) )
                        visited_pair_list.append( (o, s) )

                elif reverse_cardinality > 1:
                    print ('ERROR: there are multiple rdfs:subClassOf edges: ', reverse_cardinality)
                    print (s, '\t and \t',o)
                    for (s_tmp, p_tmp, o_tmp) in reverse_subclass_triples:
                        print ('s = ', s_tmp)
                        print ('p = ', p_tmp)
                        print ('o = ', o_tmp)



        print ('count total pairs = ', count)
        print ('count removed = ', count_removed)
        print (cnt_removed)
        print ('count left = ', count_left)
        print (cnt_left)
        print ('count right = ', count_right)
        print (cnt_right)
        print ('===both====')
        print (cnt_both)
        print ('===both====')
        print ('count equivalent class = ', count_sameas)
        print (cnt_sameas)
        print ('count undecided/unknown', count_unknown)
        print (cnt_unknown)


if __name__ == "__main__":
   generate()

#    load()
    # generate_reduced()
