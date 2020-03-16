# simplify these cycles

from z3 import *

from hdt import HDTDocument, IdentifierPosition
import networkx as nx
import sys
import csv
import time
from collections import Counter
import tldextract
import json
from bidict import bidict
import matplotlib.pyplot as plt

start = time.time()

# for plotting
G = nx.DiGraph()
found_cycles = []
result_edges = []
#
# reduced = open(csv_filename, newline='')
# reader = csv.DictReader(reduced)

# PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
# hdt_lod = HDTDocument(PATH_LOD)
# hdt_file = hdt_lod

# define propositional variable
count = 0
nodes = set()

encode = {}  # a dictionary for this encodeing of pairs
encode_index = 0

record_super = {}

# o = Optimize()

edges = set()

with open('other_cycles.json', newline='') as f:
    data = json.load(f)
    for cycle in data:
        clause = False #
        for i in range(len(cycle)):
            j = i +1
            if j == len(cycle):
                j =0
            # i and j
            left_string = cycle[i]
            right_string = cycle[j]
            if (left_string, right_string) not in encode:
                # encode[(left_string, right_string)] = Bool(str(encode_index))
                edges.add((left_string, right_string))
                # encode_index += 1
            #propositional variable
            # p = encode[(left_string, right_string)]
            # append the negotiation of this propositional variable
            # clause = Or(clause, Not(p))
        # o.add (clause)

g = nx.DiGraph(list(edges))
flag = True
while flag:
    try:
        cycle = nx.find_cycle(g)
        print ('find cycle', cycle)
        g.remove_edges_from(cycle)
    except:
        flag = False
