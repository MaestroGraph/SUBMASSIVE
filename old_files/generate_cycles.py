# this Python script generates loops in the LOD-a-lot knowledge graph
# the maximum depth is 77 from the paper of Luigi, so we don't examine entities
# beyond the scope of 77 steps. More specifically, we start from the foaf:Person
# entity and see how many loops there are within the scope of 77 steps.
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




error_list = []
#these two create cycles
error_list.append( ('http://xmlns.com/foaf/0.1/Person',  'http://xmlns.com/foaf/0.1/Person'))
error_list.append( ('http://sw.opencyc.org/2008/06/10/concept/en/HomoSapiens', 'http://sw.opencyc.org/2008/06/10/concept/en/Person'))
#the rest are meaningless
error_list.append( ('http://xmlns.com/foaf/0.1/Preferences', 'http://xmlns.com/foaf/0.1/Person'))
# http://xmlns.com/foaf/0.1/Preferences

# Quesiton 1: set things up
start = time.time()
# starting from the node of foaf:Person, get all its equivalent classes
existing = []
to_expand = []
# to_expand.append('http://dbpedia.org/ontology/Person')
to_expand.append('http://xmlns.com/foaf/0.1/Person')
while to_expand != []:
    for t in to_expand:
        to_expand.remove(t)
        existing.append(t)
        (triples, cardinality) = hdt_lod.search_triples(t, "http://www.w3.org/2002/07/owl#equivalentClass", "")
        for (s, p, o) in triples:
            if o not in existing:
                to_expand.append(o)
        (triples, cardinality) = hdt_lod.search_triples("", "http://www.w3.org/2002/07/owl#equivalentClass", t)
        for (s, p, o) in triples:
            if s not in existing:
                to_expand.append(s)

existing = list(set(existing))
print ('there are in total ', len(existing), ' equivalent classes')
# print (existing)



class Node(object):

    def __init__(self, n, parent = None, depth = 0):
        self.classname = n
        self.subclass = []
        self.parent = parent
        self.depth = depth
    def expand_node (self):
        # print (self.depth, ' : now expanding :', self.classname)
        (subclasstriples, cardinality) = hdt_lod.search_triples("", "http://www.w3.org/2000/01/rdf-schema#subClassOf", self.classname)
        if cardinality != 0:
            for (s, p, o) in subclasstriples:
                if s != "http://www.w3.org/2002/07/owl#Nothing" and ((s, self.classname) not in error_list):
                    nd = Node(s, parent = self, depth = self.depth+1)
                    rtn = nd.expand_node()
                    self.subclass.append(nd)


    def display (self, ind):
        print ('\t'*ind, self.classname)
        for n in self.subclass:
            n.display(ind+1)

    def to_network(self):
        l = []
        for n in self.subclass:
            l += n.to_network()
            l.append((self.classname, n.classname))
        return l

def print_path(node):
    if (node != None):
        print (node.depth,'\t', node.classname)
        node = node.parent
        print_path(node)

tree = Node('root')
for e in existing:
    print ('create node :', e)
    node_e = Node(e, parent=tree, depth = 1)
    end = node_e.expand_node()
    tree.subclass.append(node_e) # all the above

print ('=============print tree============')
tree.display(0)

l = tree.to_network()
# then convert to a directed network
print ('list size: ', len(l))
g = nx.DiGraph(l)
print ('print cycles ==== ')
print(list(nx.simple_cycles(g)))
# print (nx.cycle_basis(g.to_undirected()))

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Q10: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
