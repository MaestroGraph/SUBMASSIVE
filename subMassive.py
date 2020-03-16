# SUBMASSIVE
# Shuai Wang
# shuai.wang@vu.nl
# All rights reserved.
# =====
# this is the main script of the SUBMASSIVE system.
# it includes the functionality of HDT (interaction with a knowledge graph),
# and networkx (for the analysis of graphs) and Z3 (MAXSAT solver). As a result,
# it is heavy for the memory. Thus, the use of the output files of SUBMASSIVE will
# be implemented in the near future in another script.

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
import json
import random
from equiClass import equiClassManager
import random

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
PATH_EQ = "term2id_0-99.csv"

class SubM:

    # Initializer
    def __init__(self, path_hdt = PATH_LOD, path_eq = PATH_EQ):
        self.hdt = HDTDocument(path_hdt)
        self.subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
        self.id_subClassOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)
        self.equivalent = "http://www.w3.org/2002/07/owl#equivalentClass"
        self.id_equivalentClass = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentClass", IdentifierPosition.Predicate)

        self.graph = nx.DiGraph()

        self.equi_graph_manager = None #equiClassManager(path_eq)
        self.diagnosed_relations = [] # the result
        self.suggestion_on_relations = [] # from the manual decison and Joe's sameAs data. Triple
        self.leaf_classes = set()

    # the graph includes all the triples with subClassOf as predicate
    def setup_graph(self):
        (subclass_triple_ids, cardinality) = self.enquiry(query = (0, self.id_subClassOf, 0), mode = "default")
        collect_pairs = []
        for (s_id, _, o_id) in subclass_triple_ids:
            # add to the directed graph
            collect_pairs.append((s_id, o_id))
        self.graph.add_edges_from(collect_pairs)

    # for the sake of effeciency, we remove all the leaf nodes of the graph (classes
    # that does not have subclasses. They don't participate in any cycle by definition)
    def filter_leaf_classes (self):
        for c in self.graph.nodes:
            #test if this node is a leaf
            (_, cardi) = self.enquiry (query = (0, self.id_subClassOf, c), mode = "default")
            if cardi == 0:
                self.leaf_classes.add(c)
        print ('there are a total of', len(self.leaf_classes), 'leaf nodes removed')
        for c in self.leaf_classes:
            self.remove_class(c)

    # a similar funtion as that of networkx
    def remove_class(self, c, comment='remove'):
        if self.graph.has_node(c):
            self.graph.remove_node(c) # this also removes all the edges related
            # self.diagnosed_classes[c]= comment
        # automatically,  remove the related edges connected

    # a similar funtion as that of networkx
    def remove_class_from (self, cs, comment='remove'):
        for c in cs:
            self.remove_class(c, comment)

    # This is for future use of the SUBMASSIVE system. A user may ignore this for now.
    def enquiry(self, query, mode = "subm"):
        (s, p, o) = query
        if mode == "default":
            return self.hdt.search_triples_ids(s, p, o)
        else:
            # examine the filtered part first
            pass

    # Similar as that of networkx
    def remove_relation(self, sub, sup, comment = 'remove'):
        if self.graph.has_edge(sub, sup):
            self.graph.remove_edge(sub, sup)
            self.diagnose_relations(sub, sup, comment)

    # Similar as that of networkx
    def remove_relation_from (self, relation_list, comment = 'remove'):
        for (sub, sup) in relation_list:
            self.remove_relation(sub, sup, comment)

    # there is only one term that has different id when retrieved as Subject or Object
    def convert_to_id(self, term):
        if term == "akt742:Intangible-Thing":
            # this is the only class that has two different ids (as subject and object)
            return 2601100675
        else:
            return self.hdt.convert_term(term, IdentifierPosition.Subject)
    # there is only one term that has different id when retrieved as Subject or Object
    def convert_to_term(self, id):
        if id == 2601100675:
            return "akt742:Intangible-Thing"
            # this is the only one that has two different ids (as subject and object)
        else:
            return self.hdt.convert_id(id, IdentifierPosition.Subject)

    # remove the reflexive edges
    def filter_reflexsive(self):
        to_remove = set()
        file =  open('reflexive.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT", "SUGGESTION", "DECISION"])
        for e in self.graph.edges():
            (l, r) = e
            if l == r:
                to_remove.add(e)
        print('Number of removed reflexive relations', len(to_remove))
        for (l, r) in to_remove:
            l_term = self.convert_to_term(l)
            r_term = self.convert_to_term(r)
            writer.writerow([l, l_term, r, r_term, 'remove', 'o'])

        self.graph.remove_edges_from(list(to_remove))

    def print_graph_info (self):
        print ('there are ', len(self.graph.nodes()), ' nodes')
        print ('there are ', len(self.graph.edges()), ' edges')

    # compare against the owl:sameAs relations and rdfs:equivalentClass relations
    # at each iteration, if there is such a edge, then remove this one.
    def obtain_unnecessary_relations(self):
        to_remove = set()
        file =  open('equivalent-unnecessary-relations.csv', 'w', newline='')
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT", "SUGGESTION", "DECISION"])
        count_i = 0
        count_s = 0
        for e in self.graph.edges():
            label = ''
            (l, r) = e
            # convert to terms
            l_term = self.convert_to_term(l)
            r_term = self.convert_to_term(r)

            # Step 1: Equicalence Class
            (eq_triple_ids, cardinality1) = self.enquiry(query = (l, self.id_equivalentClass, r), mode = "default")
            (eq_triple_ids, cardinality2) = self.enquiry(query = (r, self.id_equivalentClass, l), mode = "default")


            if (cardinality1 == 1 or cardinality2 == 1):
                label = 'i'
                count_i += 1
            # Step 2: owl:sameAs
            if (self.equi_graph_manager.test_equivalent(l_term, r_term)):
                label += 's'
                count_s += 1
            if label != '':
                to_remove.add(e)
                writer.writerow([l, l_term, r, r_term, 'remove', label])
        print ('count_s = ', count_s)
        print ('count_i = ', count_i)
        print('Number of removed unnecessary relations', len(to_remove))
        self.graph.remove_edges_from(list(to_remove))

    # for the sake of memory effeciency, we can load these unnecessary relations directly
    # this is because the sameas data is very big.
    def load_unnecessary_relations (self): # to self.suggestion_on_relations
        eq_file = open('equivalent-unnecessary-relations.csv', 'r')
        reader = csv.DictReader(eq_file)
        for row in reader:
            s_id = int(row["SUBJECT_ID"])
            o_id = int(row["OBJECT_ID"])
            sug = row["SUGGESTION"] # should be remove
            self.suggestion_on_relations.append((s_id, o_id,  sug))
        print (len(self.suggestion_on_relations), ' total  relations loaded')

    # load the manual decisions on size-two cycles
    def load_manually_decided_relations(self): # to self.suggestion_on_relations
        man_file = open('lod-two-cycle.csv', 'r')
        reader = csv.DictReader(man_file)
        coll_nodes = []
        for row in reader:
            s_id = int(row["SUBJECT_ID"])
            # s = row["SUBJECT"]
            o_id = int(row["OBJECT_ID"])
            sug = row["SUGGESTION"]
            coll_nodes.append(s_id)
            coll_nodes.append(o_id)
            self.suggestion_on_relations.append((s_id, o_id, sug))
        print (len(self.suggestion_on_relations), ' total relations loaded')
        return coll_nodes

    def find_nodes_in_cycles(self, hint_nodes, max, found_min):
        # create a new graph
        tmp_graph = self.graph.copy()
        # find each node that participate in at least one cycle:
        nodes = set()

        flag = True # flag for debugging
        count_found_cycles = 0
        while flag:
            try:
                c = []
                hint_not_working = False #flag
                try:
                    c = nx.find_cycle(tmp_graph, hint_nodes) # change to simple_cycles ??

                except Exception as e:
                    hint_not_working = True

                if hint_not_working :
                    c = nx.find_cycle(tmp_graph)
                count_found_cycles += 1
                print ('Found Cyclce ',count_found_cycles, ' is: ', c)
                c_nodes = [x for (x, y) in c]

                (l_tmp, r_tmp) = random.choice(c)
                tmp_graph.remove_edge(l_tmp, r_tmp)
                nodes.update(c_nodes)
                if len(nodes) >= max and count_found_cycles >= found_min:

                    print ('total nodes = ', len(nodes))
                    flag = False
                else:
                    nodes.update(c_nodes)
                    hint_nodes = c_nodes + hint_nodes
            except Exception as e:
                print (e)
                # print("There is no cycle anymore")
                flag = False

        nodes = list (nodes)
        print ('there are in total ', len (nodes), '  nodes that participate in cycles')
        print (nodes)
        return nodes

    def get_cycles_from_nodes(self, nodes):
        coll_cycles = [] # a list, not a set
        # obtain a subgraph from the nodes
        subg = self.graph.subgraph(nodes)

        simp_c = list(nx.simple_cycles(subg))
        print (' and these nodes has ', len(simp_c), ' simple cycles among them')
        # next, process these cycles and get ready to encode
        for c in simp_c:
            if  len (c) == 2:
                (l, r) = c
                coll_cycles.append([(l,r), (r, l)])
            else:
                # print ('original = ', c)
                cycle = []
                for i in range(len(c)):
                    j = i + 1
                    if i == len (c) - 1:
                        j = 0
                    cycle.append((c[i], c[j]))
                # print ('cycle = ', cycle)
                coll_cycles.append( cycle )
        return (coll_cycles)




        return coll_cycles # get ready for encoding



def main ():

    start = time.time()
    # ==============
    # some small tests
    sm = SubM()
    print ('finished initialization')
    sm.setup_graph()
    print ('after setting up the graph:')
    sm.print_graph_info()

    # PRE-PROCESSING
    # 1) Filter Leaf nodes
    sm.filter_leaf_classes()
    print ('after filtering leaf nodes')
    sm.print_graph_info()

    # 2) Filter reflexive nodes
    sm.filter_reflexsive()
    print ('after removing reflexive edges:')
    sm.print_graph_info()


    #  OUTDATED # 3) Filter the unnecessary relations
    # sm.obtain_unnecessary_relations()
    # print ('do you want to continue?')
    # input()
    # print ('after exporting unnecessary relations (regarding SameAs data)')
    # s.print_graph_info()



    # 4) load the data from Joe's equivalent classes and my manual decisions
    sm.load_unnecessary_relations()


    # print ('remove a total of ', len(sm.suggestion_on_relations), ' relations to remove')
    count = 0
    count_remove_sug = 0
    for (s_id, o_id, sug) in sm.suggestion_on_relations:

        if sug == 'remove':
            if sm.graph.has_edge(s_id, o_id):
                sm.graph.remove_edge(s_id, o_id)
                count_remove_sug += 1
            else:
                count += 1
                # print ('removing not existing relation: ',s_id, o_id)
    print ('count (remove edges from  suggestion) = ', count_remove_sug)
    print ('count (not existing) = ', count)

    coll_nodes = sm.load_manually_decided_relations()

    # # 5) == remove start =
    # find all the nodes
    max = int(sys.argv[1])
    found_min = int(sys.argv[2])
    run = int(sys.argv[3])
    print ('This cycle takes ', max, ' as the upper bound')
    nodes = sm.find_nodes_in_cycles(coll_nodes, max, found_min)
    cycle_samples = sm.get_cycles_from_nodes(nodes)

    # export all the cycles
    # print ('These cycles are\n',cycle_samples)
    cycle_outfile =  open('cycles_resolved.txt', 'w')
    # json.dump(cycle_samples, cycle_outfile)
    collect_all_resolved_cycles = cycle_samples
    collect_final_removed_edges = set()
    # file_final_removed_edges =  open('final_removed_edges.txt', 'w')

    count_round = 1
    overall_flag = True
    while (overall_flag):
        round_start = time.time()
        # ==============

        # ====
        #  Encode and decode
        # ======
        # define the propositional variables
        encode = {}
        for c in cycle_samples:
            for (l, r) in c:
                if (l,r) not in encode.keys():
                    encode[(l, r)] = Bool(str(l)+ str(r))

        o = Optimize()
        for c in cycle_samples:
            clause = False
            for (l, r) in c:
                p = encode [(l, r)]
                clause = Or(clause, Not(p))
            o.add(clause)

        for e in encode:
            o.add_soft(encode[e], 1)
        # each cycle, there is at least one

        print(o.check())
        # print(o.model())
        m = o.model()

        # for c in cycle_samples:
            # print ('\n\nfor this cycle: ',c)
            # print ('the edges are like:')
        for e in encode.keys():
            (l,r) = e
            e = (l, r)
            # print ('l: ', l , ' = ', sm.convert_to_term(l))
            # print ('r: ', r , ' = ', sm.convert_to_term(r))
            # print (e, 'assigns to' , m.evaluate(encode[e]))
            if (m.evaluate(encode[e]) == False):
                # print ('remove this edge')
                if sm.graph.has_edge(l, r):
                    sm.graph.remove_edge(l,r)
                    collect_final_removed_edges.add(e)

        collect_all_resolved_cycles += cycle_samples
        # print ('TOTOAL RESOLVED CYCLES = ', len (collect_all_resolved_cycles))
        print ('TOTOAL REMOVED EDGES =  ', len(collect_final_removed_edges))


        # finally, check if there are still cycles
        # print ('Finally test if there are still cycles:')
        #
        # print ('1) first test if are cycles involving the nodes we had:')
        # verify_cycle_samples = sm.get_cycles_from_nodes(nodes)
        # print ('they are:',verify_cycle_samples)
        #
        count_round +=1
        print('\n\n******************\n THIS IS ROUND: ', count_round)
        c = []
        try:
            c = nx.find_cycle(sm.graph)
        except Exception as e:
            overall_flag = False
        # print ('2) then test if are cycles from the graph:')
        # cycle_samples = nx.find_cycle(sm.graph)
        c_nodes = [x for (x, y) in c]
        nodes = sm.find_nodes_in_cycles(nodes + coll_nodes + c_nodes, max, found_min)
        cycle_samples = sm.get_cycles_from_nodes(nodes)
        if len (cycle_samples) == 0:
            cycle_samples = [c]
        # ===============
        round_end = time.time()
        hours, rem = divmod(round_end - round_start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("This round takes time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))



# after all this, we print all the removed edges.
    print ('After ', count_round, ' rounds')
    print ('\tNo. total removed = ', len(collect_final_removed_edges))
    print ('\tNo. total cycles resolved = ', len(collect_all_resolved_cycles))
    # json.dump(list(collect_final_removed_edges), file_final_removed_edges)
    json.dump(collect_all_resolved_cycles, cycle_outfile)

    # ===============
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


    file_name = 'final_removed_edges_' + str(max) +':'+ str(run) +'_'+ str(len(collect_final_removed_edges)) + str('_{:0>2}:{:0>2}:{:05.2f}'.format(int(hours),int(minutes),seconds)) + '.csv'
    print ('export to ', file_name)
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "SUBJECT", "OBJECT_ID", "OBJECT", "SUGGESTION", "DECISION"])
        # write to file
        for (s_id, o_id) in collect_final_removed_edges:
            # convert
            s_term = sm.convert_to_term(s_id)
            o_term = sm.convert_to_term(o_id)
            writer.writerow([s_id, s_term, o_id, o_term, 'remove', 'a'])  # removed from automatic method


if __name__ == "__main__":
    main()
