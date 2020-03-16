# Shuai Wang @ VU Amsterdam
# This is a wrapper class of the hdt Python library with networkx functions
# it maintains a network of subclassof relations

from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
import datetime
import pickle
import time
import networkx as nx
import sys
import csv
from z3 import *
from bidict import bidict
import matplotlib.pyplot as plt
import tldextract

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"

class SubM:

    # Initializer / Instance Attributes
    def __init__(self, path_hdt = PATH_LOD):
        self.hdt = HDTDocument(path_hdt)
        self.subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
        self.id_subClassOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
        self.equivalent = "http://www.w3.org/2002/07/owl#equivalentClass"
        self.id_equivalentClass = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentClass", IdentifierPosition.Predicate)
        self.graph = nx.DiGraph()
        self.equi_graph = nx.Graph()
        self.diagnosed_relations = {}
        self.diagnosed_classes = {}
        self.leaf_classes = set()

    def setup_graph(self):
        (subclass_triple_ids, cardinality) = self.enquiry(query = (0, self.id_subClassOf, 0), mode = "default")
        collect_pairs = []
        for (s_id, _, o_id) in subclass_triple_ids:
            # add to the directed graph
            collect_pairs.append((s_id, o_id))
        self.graph.add_edges_from(collect_pairs)

    def remove_unnecessary_relations(self):
        for n in self.graph.nodes():
            # test if there is an edge between this node and another node which is also in the Graph
            (eq_triple_ids, cardinality) = self.enquiry(query = (n, self.id_equivalentClass, 0), mode = "default")
            for (_,_,m) in eq_triple_ids:
                # test if it is in the Graph
                if m in self.graph.nodes():
                    self.remove_relation(n, m, 'equivalence')
            (eq_triple_ids, cardinality) = self.enquiry(query = (0, self.id_equivalentClass, n), mode = "default")
            for (m,_,_) in eq_triple_ids:
                # test if it is in the Graph
                if m in self.graph.nodes():
                    self.remove_relation(m, n, 'equivalence')
        print ('total relations diagnosed:', len(self.diagnosed_relations))



    def export_graph(self, export_file = None):
        collect_pairs = self.graph.edges
        if export_file is not None:
            file = open(export_file, 'w', newline='')
            writer = csv.writer(file)
            writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT"])
            for (s_id, o_id) in  collect_pairs:
                s_term = self.convert_to_term(s_id)
                o_term = self.convert_to_term(o_id)
                writer.writerow([s_term, s_id, o_term, o_id])

    # define a function subgraph, edges
    # G.edges
    # https://networkx.github.io/documentation/stable/reference/classes/generated/networkx.DiGraph.edges.html#networkx.DiGraph.edges

    def remove_all_two_cycles(self):
        to_remove = set ()
        for (l, r) in self.graph.edges():
            if (r, l) in self.graph.edges():
                to_remove.add((l,r))
                to_remove.add ((r,l))
        print ('there are in total', len(to_remove), ' two-cycle edges removed')
        for (l,r) in to_remove:
            self.graph.remove_edge(l,r)

    def load_manual_decisions(self, file, mode = "remove"):
        #if mode = ignore, then we don't do anything to those marked as unknown
        #if mode = remove, then we remove all those that are unknown
        l_two = []
        two = open(file, newline='')
        reader_two = csv.DictReader(two)
        for row in reader_two:
            if (row['SUBJECT_ID'], row['OBJECT_ID']) not in self.diagnosed_relations.keys():
                if (row['SUGGESTION'] == 'remove'):
                    self.remove_relation(row['SUBJECT_ID'], row['OBJECT_ID'], comment = 'remove')
                else:
                    self.diagnosed_relations[row['SUBJECT_ID'], row['OBJECT_ID']] = row['SUGGESTION']
            # l_two.append((row['SUBJECT_ID'], row['OBJECT_ID']))
        # if it is labeled as 'remove' then remove,
        # if it is labeled as 'unknown' then depends on the mode it is in
        print ('there are in total ', len(l_two), ' relations removed from mannual decisions')
        self.graph.remove_edges_from(l_two)


    def enquiry(self, query, mode = "subm"):
        (s, p, o) = query
        if mode == "default":
            return self.hdt.search_triples_ids(s, p, o)
        else:
            # examine the filtered part first
            pass


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

    def remove_relation(self, sub, sup, comment = 'remove'):
        if self.graph.has_edge(sub, sup):
            self.graph.remove_edge(sub, sup)
            self.diagnose_relations(sub, sup, comment)

    def remove_relation_from (self, relation_list, comment = 'remove'):
        for (sub, sup) in relation_list:
            self.remove_relation(sub, sup, comment)

    def diagnose_relations(self, sub, sup, comment='default'):
        self.diagnosed_relations[(sub, sup)] = comment
        # change it to a dictionary?


    def diagnose_class(self, c, comment='default'):
        self.diagnosed_class[c] = comment

        # TODO, split the cases of removal and comment

    def remove_class(self, c, comment='remove'):
        if self.graph.has_node(c):
            self.graph.remove_node(c) # this also removes all the edges related
            self.diagnosed_classes[c]= comment
        # TODO, also remove the related edges connected

    def remove_class_from (self, cs, comment='remove'):
        for c in cs:
            self.remove_class(c, comment)

    def filter_leaf_classes (self):
        count = len(self.diagnosed_classes)

        for c in self.graph.nodes:
            #test if this node is a leaf
            (_, cardi) = self.enquiry (query = (0, self.id_subClassOf, c), mode = "default")
            if cardi == 0:
                self.leaf_classes.add(c)
        for c in self.leaf_classes:
            self.remove_class(c)
        print ('there are a total of', len(self.diagnosed_classes) - count, 'leaf nodes removed')

    def get_domain_from_id(self, id):
        t = self.convert_to_term(id)
        return tldextract.extract(t).domain

    def filter_domain_classes(self, domain):
        filtered = set()
        for c in self.graph.nodes:
            t = self.convert_to_term(c)
            if (domain == tldextract.extract(t).domain):
                filtered.add(c)
        print ('a total of ', len (filtered), ' removed w.r.t. domain ', domain)
        self.remove_class_from(list(filtered))

    def filter_reflexsive(self):
        to_remove = set()
        for e in self.graph.edges():
            (l, r) = e
            if l == r:
                to_remove.add(e)
        print('removed reflexive relations', len(to_remove))
        self.graph.remove_edges_from(list(to_remove))

    def print_cycles (self):
        count = 0
        flag = True
        while flag:
            try:
                cycle = nx.find_cycle(self.graph)
                print ('find cycle', cycle)
                (l,r) = cycle[0]
                print (self.get_domain_from_id(l))
                self.graph.remove_edges_from(cycle)
            except Exception as e:
                print (e)
                flag = False

    # def shrink_graph(self):
    #     output_filename = "term2id_subM.csv"
    #     file2 = open(output_filename, 'w', newline='')
    #     writer = csv.writer(file2)
    #     writer.writerow([ "TERM", "GROUPID"])
    #
    #     file_name = "term2id.csv"
    #     count_in = 0
    #     count = 0
    #     with open(file_name, 'r') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             count +=1
    #             # print ('term   :', row["TERM"])
    #             # print ('groupid:', row["GROUPID"])
    #             if (row["TERM"] in self.graph.nodes()):
    #                 count_in +=1
    #                 print ('in this graph is ', row["TERM"])
    #                 writer.write ([row["TERM"], row["GROUPID"]])
    #     print ('among a total of ', count)
    #     print (count_in, ' are there in our subM graph')

def main ():
    # some small tests
    s = SubM()
    s.setup_graph()
    s.filter_reflexsive()
    # s.remove_all_two_cycles()
    # s.shrink_graph()
    s.remove_unnecessary_relations()
    s.load_manual_decisions("lod-two-cycle.csv")
    print (s.diagnosed_relations)
    # s.export_graph(export_file = 'export_graph.csv')
    # s.filter_leaf_classes()

    # s.filter_domain_classes('carleton')
    # s.filter_domain_classes('dbpedia')
    # s.filter_domain_classes('creationwiki')
    # s.filter_domain_classes('umbel')
    # s.filter_domain_classes('co-ode')
    # s.filter_domain_classes('micra')
    # s.filter_domain_classes('opencyc')
    # s.filter_domain_classes('a')
    # s.filter_domain_classes('obofoundry')
    # s.filter_domain_classes('purl')
    # s.filter_domain_classes('owl-ontologies')
    # s.filter_domain_classes('mygrid')
    # s.filter_domain_classes('a')


    # s.print_cycles()
    #
    # print ('before closure, there are in total ', s.graph.size())
    #
    # print ('========TRANSITIVE CLOSURE==========')
    # s.graph = nx.transitive_closure(s.graph)
    # print ('after closure, there are in total ', s.graph.size())
    # s.print_cycles()




if __name__ == "__main__":
    main()
