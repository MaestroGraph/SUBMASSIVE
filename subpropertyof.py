# SUBMASSIVE
# Shuai Wang
# shuai.wang@vu.nl
# All rights reserved.
# =====
# This file is for that of subPropertyOf
# it turned out that the case is much simpler than that of subclassof. 
# this file tests if there is any cycle in the graph and export the graph.



from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
import datetime
import pickle
import time
import networkx as nx
import sys
import csv
# from z3 import *
from bidict import bidict
import matplotlib.pyplot as plt
import tldextract
import json
import random
from equiClass import equiClassManager
# import random
# from rdflib import Graph
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt" # a user would need to update this
PATH_EQ = "term2id_0-99.csv" # not used in this file
file_name = 'pre-subP.csv' # this includes your decision about the cycles as well as the reflexive edges



class SubP:

    # Initializer / Instance Attributes
    def __init__(self, path_hdt = PATH_LOD, path_eq = PATH_EQ):
        self.hdt = HDTDocument(path_hdt)

        self.subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
        self.id_subClassOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)

        self.equivalent = "http://www.w3.org/2002/07/owl#equivalentClass"
        self.id_equivalentClass = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentClass", IdentifierPosition.Predicate)

        self.subPropertyOf = "http://www.w3.org/2000/01/rdf-schema#subPropertyOf"
        self.id_subPropertyOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subPropertyOf", IdentifierPosition.Predicate)

        self.equivalentProperty = "http://www.w3.org/2002/07/owl#equivalentProperty"
        self.id_equivalentProperty = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentProperty", IdentifierPosition.Predicate)


        self.graph = nx.DiGraph()

        self.equi_graph_manager = None #equiClassManager(path_eq)
        print ('set up the equivalence class manager')
        self.diagnosed_relations = [] # the result
        self.suggestion_on_relations = [] # from the manual decison and Joe's sameAs data. Triple
        self.leaf_classes = set()

        print ('finished initialization')

    def setup_graph(self):
        print('set up the graph')
        (subclass_triple_ids, cardinality) = self.enquiry(query = (0, self.id_subPropertyOf, 0), mode = "default")
        collect_pairs = []
        for (s_id, _, o_id) in subclass_triple_ids:
            # add to the directed graph
            collect_pairs.append((s_id, o_id))

        print ('there are ', len (collect_pairs), 'edges')
        self.graph.add_edges_from(collect_pairs)


    def convert_to_id(self, term):
        if term == "akt742:Intangible-Thing":
            # this is the only class that has two different ids (as subject and object)
            return 2601100675
        else:
            return self.hdt.convert_term(term, IdentifierPosition.Subject)

    def convert_to_term(self, id):
        if id == 2601100675:
            return "akt742:Intangible-Thing"
            # this is the only one that has two different ids (as subject and object)
        else:
            return self.hdt.convert_id(id, IdentifierPosition.Subject)

    def enquiry(self, query, mode = "subp"):
        (s, p, o) = query
        if mode == "default":
            return self.hdt.search_triples_ids(s, p, o)
        else:
            # examine the filtered part first
            pass


    def print_info(self, sbj, obj):
        predicate_names = [
        "http://sw.cyc.com/CycAnnotations_v1#label",
        "http://www.w3.org/2000/01/rdf-schema#comment",
        "http://www.w3.org/2000/01/rdf-schema#label"
        ]

        s_domain = tldextract.extract(sbj).domain
        o_domain = tldextract.extract(obj).domain
        # filter that domain
        # if (s_domain != DOMAIN and o_domain != DOMAIN):
        #     # print (DOMAIN)
        print ('SUBJECT: ', sbj)
        for p in predicate_names:
            (triples, cardinality) = self.hdt.search_triples(sbj, p, "")
            for (s, p, o) in triples:
                print ('\tPREDICATE: ', p)
                print ('\t\t Comments/labels  :', o,'\n')
        print ('OBJECT: ', obj)
        for p in predicate_names:
            (triples, cardinality) = self.hdt.search_triples(obj, p, "")
            for (s, p, o) in triples:
                print ('\tPREDICATE: ', p)
                print ('\t\t Comments/labels  :', o,'\n')

        print ('\n\n========================\n\n')




    def export_cycle(self):
        simp_c = list(nx.simple_cycles(self.graph))
        print('find simple cycle in graph')
        print ('there are ', len (simp_c), ' simple cycles')

        count1 = 0
        count_others = 0
        count_sameas = 0
        count_eqProp = 0
        count_bigger = 0

        collect_self_loop = []
        collect_eq = []
        collect_others = []
        collect_bigger = []
        for c in simp_c:
            if len (c) == 1:
                count1 += 1
                collect_self_loop.append(c)
            elif len (c) == 2:
                # print (c)
                # for n in c:
                #     t = self.convert_to_term(n)
                #     print ('\t', t)
                # print ('\n')

                l_term = self.convert_to_term(c[0])
                r_term = self.convert_to_term(c[1])

                # id_equivalentProperty
                (subclass_triple_ids, cardinality) = self.enquiry(query = (c[0], self.id_equivalentProperty, c[1]), mode = "default")

                # if (self.equi_graph_manager.test_equivalent(l_term, r_term)):
                #     print ('There is a owl:sameAs relation in between')
                #     count_sameas += 1
                #     collect_eq.append(c)

                if (cardinality > 0):
                    print ('There is a owl:equivalentProperty in between')
                    count_eqProp += 1
                    collect_eq.append(c)

                else:
                    # self.print_info(c[0], l_term, c[1], r_term)
                    # print ('a longer one for manual decision:',c )
                    # count_others += 1
                    collect_others.append(c)
                count_others += 1
            else:
                count_bigger += 1
                collect_bigger.append( ( c[0],c[1]))
                collect_bigger.append( ( c[1],c[2]))
                collect_bigger.append((c[2],c[0]))


        print ('there are ', count1,  ' reflexive cycles')

        print ('there are ', count_sameas, ' sameAs relations')
        print ('there are ', count_eqProp, ' eqProp relations')
        print ('there are ', count_others,  ' size-two cycles')
        print ('there are ', count_bigger,  ' bigger cycles')
        # export self-loop cycles:

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT", "SUGGESTION", "DECISION"])
            # write to file
            # print ('collect self loop: ',collect_self_loop)
            for [s_id] in collect_self_loop:
                # convert
                s_term = self.convert_to_term(s_id)
                o_term = s_term
                writer.writerow([s_id, s_term, s_id, o_term, 'remove', 'o'])  # removed from automatic method
            for (s_id, o_id) in collect_eq:
                # convert
                s_term = self.convert_to_term(s_id)
                o_term = self.convert_to_term(o_id)
                writer.writerow([s_id, s_term, o_id, o_term, 'remove', 'e'])  # removed from automatic method

            for (s_id, o_id) in collect_others:
                s_term = self.convert_to_term(s_id)
                o_term = self.convert_to_term(o_id)
                self.print_info(s_term, o_term)
                writer.writerow([s_id, s_term, o_id, o_term, 'remove', '2'])  # removed from manual step
                writer.writerow([ o_id, o_term,s_id, s_term, 'remove', '2'])  # removed from manual step


            for (s_id, o_id) in collect_bigger:
                s_term = self.convert_to_term(s_id)
                o_term = self.convert_to_term(o_id)
                # print ('===a longer cycle ===', c)

                writer.writerow([s_id, s_term, o_id, o_term, 'remove', 'x'])  # removed from manual step

    def load_removed(self):
        # 'pre-subP.csv'
        subp_file = open('pre-subP.csv', 'r')
        reader = csv.DictReader(subp_file)
        coll_removed = []
        for row in reader:
            s_id = int(row["SUBJECT_ID"])
            # s = row["SUBJECT"]
            o_id = int(row["OBJECT_ID"])
            sug = row["SUGGESTION"] # should be remove

            if (sug == 'remove'):
                coll_removed.append((s_id, o_id))
        print ('number of removed edges:', len(coll_removed))
        self.graph.remove_edges_from(coll_removed)




    def test_cycle(self):
        try:
            c = nx.find_cycle(self.graph) # change to simple_cycles ??
            print ('cycle = ', c)

        except Exception as e:
            # hint_not_working = True
            print ('no cycle')

    def export_graph_nt(self, name):
        g = Graph()
        for (s_id, o_id) in self.graph.edges:
            s_term = self.convert_to_term(s_id)
            o_term = self.convert_to_term(o_id)
            bob = URIRef("http://www.w3.org/2000/01/rdf-schema#subPropertyOf")
            g.add( (URIRef(s_term), bob , URIRef(o_term)))

        # print("--- printing raw triples ---")
        # for s, p, o in g:
        #     print((s, p, o))

        g.serialize(destination=name, format='nt')
        # file = open(name,'w')
        # txt = g.serialize(format='nt')
        # file.write(txt)
        # file.close()



def main ():
    print ('start')
    start = time.time()
    # ==============
    # some small tests
    sp = SubP()

    sp.setup_graph()
    sp.export_graph_nt('subP-all.nt')
    # subP-all
    # sp.export_cycle()
    sp.load_removed()
    sp.test_cycle()
    sp.export_graph_nt('refined-subP.nt')



if __name__ == "__main__":
    main()
