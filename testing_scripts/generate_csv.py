# SUBMASSIVE
# Shuai Wang
# shuai.wang@vu.nl
# All rights reserved.
# =====
# ================================================================
# This file does the following things:
# 1) retrieve the subClassOf relation in csv file (from LOD-a-lot)
# 2) filter out the cycles mannually

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


def generate():
    hdt_file = None
    output_filename = None
    if sys.argv [1] == 'lod':
        hdt_file = HDTDocument(PATH_LOD)
        output_filename = 'all_lod_subClassOf.csv'

    else:
        hdt_file = HDTDocument(PATH_DBpedia)
        output_filename = 'all_dbpedia_subClassOf.csv'

    subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    id_subClassOf = hdt_file.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
    count = 0
    with open(output_filename, 'w', newline='') as file:
        (subclass_triples, cardinality) = hdt_file.search_triples("", subClassOf, "")
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT"])
        for (s, p, o) in subclass_triples:
            # store it in a csv file
            s_id = hdt_file.convert_term(s, IdentifierPosition.Subject)
            o_id = hdt_file.convert_term(o, IdentifierPosition.Object)
            writer.writerow([s_id, s, o_id, o])
            # print ([s_id, s, o_id, o])
            count += 1
    print ('total entries = ', count)


def generate_reduced():
    # Q1 : retrieve the subClassOf relations
    # hdt_file = None
    # output_filename = None
    # output_selfloopClass_filename = None
    # output_leafClass_filename = None
    # output_intermediateClass_filename = None

    # if sys.argv [1] == 'lod':
    hdt_file = HDTDocument(PATH_LOD)
    # output_filename = 'reduced_lod_subClassOf.csv'
    output_selfloopClass_filename = 'lod_reflexive_classes.csv'
    output_leafClass_filename = 'lod_leaf_classes.csv'
    # output_intermediateClass_filename = 'further_reduced_lod_subClassOf.csv'
    output_intermediateClass_filename = 'further_reduced_lod_subClassOf.csv'
    # else:
    #     hdt_file = HDTDocument(PATH_DBpedia)
    #     output_filename = 'dbpedia_subClassOf.csv'
    #     output_selfloopClass_filename = 'dbpedia_selfloop_classes.csv'
    #     output_leafClass_filename = 'dbpedia_leaf_classes.csv'
    #     output_intermediateClass_filename = 'further_reduced_dbpedia_subClassOf.csv'

    subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    id_subClassOf = hdt_file.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
    count = 0
    count_selfloop = 0
    count_leaf = 0
    count_left = 0
    count_output_after_further_reduced = 0 # count left of the further reduced
    # removed_leaf_classes = []
    (subclass_triples, cardinality) = hdt_file.search_triples("", subClassOf, "")

    to_explore_ids = set() # to iterate through
    leaf_ids = set()
    removed_intermediate_ids = set() # removed intermediate nodes
    all_ids = set()
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT"])
        with open(output_intermediateClass_filename, 'w', newline='') as inter_file:
            writer_inter = csv.writer(inter_file)
            writer_inter.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT"])

            # Step 1: remove selfloops and leaf nodes
            with open(output_selfloopClass_filename, 'w', newline='') as selfloop_file:
                writer_selfloop = csv.writer(selfloop_file)
                writer_selfloop.writerow([ "ID", "URI"])

                with open(output_leafClass_filename, 'w', newline='') as leaf_file:
                    writer_leaf = csv.writer(leaf_file)
                    writer_leaf.writerow([ "ID", "URI"])


                    for (s, p, o) in subclass_triples:
                        s_id = hdt_file.convert_term(s, IdentifierPosition.Subject)
                        o_id = hdt_file.convert_term(o, IdentifierPosition.Object)
                        all_ids.add(s_id)
                        all_ids.add(o_id)
                        count += 1
                        # store it in a csv file
                        if s == o: # self loop
                            count_selfloop += 1
                            writer_selfloop.writerow([s_id, s])
                        else:
                            (_, leaf_cardinality) = hdt_file.search_triples("", subClassOf, s)
                            # test if it is a leaf node
                            if leaf_cardinality == 0:
                                # there is no subclass, this is a leaf node/class
                                # write it to a file and store it
                                writer_leaf.writerow([s_id, s])
                                leaf_ids.add(s_id)
                                count_leaf += 1
                                # removed_leaf_classes.append(s)
                            # else:
                            #     # write what's left to the file
                            #     # SKIP: find intermediate for now
                            #     count_left += 1
                            #     writer.writerow([s_id, s, o_id, o])
            print ('count leaf statements = ', count_leaf)
            print ('count leaf (as set) = ', len (leaf_ids))
            print ('count total statements = ', count)
            print ('count_total nodes (as set) = ', len (all_ids))
            print ('NOW  Part 2: Further Reduce ') # further reduce it

            visited_sup = set()
            # near_leaf_sup = set()
            count_one = 0
            count_loop = 0
            for l_id in leaf_ids:
                count_loop += 1
                (leaf_triples, cardinality) = hdt_file.search_triples_ids(l_id, id_subClassOf, 0)
                # get its superclass id : sup_id
                finished_this_leaf = False
                if cardinality == 1:
                    (l_id, lp_id, sup_id) = leaf_triples.next()
                    (_, sub_cardinality) = hdt_file.search_triples_ids(0, id_subClassOf, sup_id)
                    if sub_cardinality == 1:
                        # remove this superclass
                        count_one += 1
                        removed_intermediate_ids.add(sup_id)
                        visited_sup.add(sup_id)
                        (supsup_triples, cardinality) = hdt_file.search_triples_ids(sup_id, id_subClassOf, 0)
                        for (sup_id, lp_id, supsup_id) in supsup_triples:
                            to_explore_ids.add(supsup_id)
                        finished_this_leaf = True

                # normal process
                if not finished_this_leaf:
                    for (l_id, lp_id, sup_id) in leaf_triples:
                        if (sup_id not in visited_sup):
                            # lo_id = hdt_file.convert_term(lo, IdentifierPosition.Object)
                            (sup_triples, cardinality_back) = hdt_file.search_triples_ids(0, id_subClassOf, sup_id)
                            supflag = True # if this superclass only has leaf nodes
                            if cardinality_back != 1:
                                for (child_id, lp_id, sup_id) in sup_triples:
                                    if child_id not in leaf_ids:
                                        sup_flag = False
                                        break

                            if supflag:
                                # near_leaf_sup.add(sup_id)
                                removed_intermediate_ids.add(sup_id)
                                (supsup_triples, cardinality) = hdt_file.search_triples_ids(sup_id, id_subClassOf, 0)
                                for (sup_id, lp_id, supsup_id) in supsup_triples:
                                    to_explore_ids.add(supsup_id)
                            else:
                                to_explore_ids.add (sup_id)
                            visited_sup.add (sup_id)

                if count_loop %100000 ==0:
                    print ('leaf nodes processed:', count_loop)
                    print ('count one = ', count_one)
                    print ('near-leaf nodes = ', len (removed_intermediate_ids))
                    print ('total visited nodes = ', len (visited_sup))
                    print ('non-near-leaf nodes = ', len(visited_sup) - len(removed_intermediate_ids))
                    print ('to explore = ', len(to_explore_ids))
            print ('*********** after this data processing, we have only ', len(to_explore_ids), ' to explore for the next step')
# # finished data- proprocessing,

            record_to_explore_size = len (to_explore_ids)
            record_iteration = 0
            continue_flag = True
            while (len(to_explore_ids) != 0 and continue_flag):
                # print ('still to explore : ', len(to_explore))
                record_iteration +=1
                # iternate through this and
                n_id = to_explore_ids.pop()
                (triples_id, cardinality) = hdt_file.search_triples_ids(0, id_subClassOf, n_id)
                flag = True
                for (ns_id, np_id, no_id) in triples_id:
                    # if each ns is either a leaf or intermediate but removed, then we remove it.
                    # ns_id = hdt_file.convert_term(ns, IdentifierPosition.Object)
                    if ns_id not in leaf_ids and ns_id not in removed_intermediate_ids:
                        # Keep it for now
                        flag = False
                        break
                if flag == True: # we are sure to remove it

                    removed_intermediate_ids.add (n_id)
                else:
                    to_explore_ids.add (n_id) # add back :(

                if record_iteration == 10000:
                    if record_to_explore_size != len (to_explore_ids):
                        # print ('leaf nodes visited = ', count_leaf)
                        print ('total leaf nodes = ', len(leaf_ids))
                        print ('accummulated removed intermediate = ', len (removed_intermediate_ids))
                        print ('still to explore  = ', len (to_explore_ids))
                        print ('record to explore = ', record_to_explore_size)
                        print ('changed = ', record_to_explore_size - len (to_explore_ids))
                        record_iteration = 0
                        record_to_explore_size = len (to_explore_ids)
                    else:
                        continue_flag = False

            # to write down the intermediate removed

            print ('*****size of leaf:', len (leaf_ids))
            print ('*****size of removed intermediate node :', len (removed_intermediate_ids))
            (subclass_triples, cardinality) = hdt_file.search_triples("", subClassOf, "")
            for (s,p,o) in subclass_triples:
                s_id = hdt_file.convert_term(s, IdentifierPosition.Subject)
                o_id = hdt_file.convert_term(o, IdentifierPosition.Object)
                # count += 1
                # store it in a csv file
                if s != o:
                    # if s is not a leaf node and not a removed intermediate node
                    if (s_id not in leaf_ids) and (s_id not in removed_intermediate_ids):
                        # write what's left to the file
                        count_output_after_further_reduced += 1
                        # print ('count output after further reduced', count_output_after_further_reduced)
                        writer_inter.writerow([s_id, s, o_id, o])
                #     else:
                #         print ('one of them')
                # else:
                #     print ('nothing')

            print ('total entries = ', count)
            print ('total self-loops = ', count_selfloop)
            print ('total leaf nodes/classes = ', count_leaf)
            print ('total left = ', count_left)
            print ('perfectage of reduction: ', count_left/count)
            print ('=====AFTER FURTHER REDUCTION ======')
            print ('There are only ', count_output_after_further_reduced)
            print ('perfectage of reduction: ', count_output_after_further_reduced/count)

def load():
    output_filename = None
    if sys.argv [1] == 'lod':
        hdt_file = HDTDocument(PATH_LOD)
        output_filename = 'all_lod_subClassOf.csv'

    else:
        hdt_file = HDTDocument(PATH_DBpedia)
        output_filename = 'all_dbpedia_subClassOf.csv'

    with open(output_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['SUBJECT_ID'], row['OBJECT_ID'])
            print(row['SUBJECT'], row['OBJECT'])
            print ('----------------------------------------------')


if __name__ == "__main__":
#    generate()
#    load()
    generate_reduced()
