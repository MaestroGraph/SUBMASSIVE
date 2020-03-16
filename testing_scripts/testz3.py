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
result_edges = []
#
# reduced = open(csv_filename, newline='')
# reader = csv.DictReader(reduced)

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt_lod = HDTDocument(PATH_LOD)
hdt_file = hdt_lod

# define propositional variable
count = 0
nodes = set()

encode = {}  # a dictionary for this encodeing of pairs
encode_index = 0

record_super = {}

o = Optimize()

with open('other_cycles.json', newline='') as f:
    data = json.load(f)
    for cycle in data:
        count += 1
        for c in cycle:
            nodes.add(int(c))
    for cycle in data:
        clause = False #
        for i in range(len(cycle)):
            j = i +1
            if j == len(cycle):
                j =0
            # i and j
            left_string = cycle[i]
            right_string = cycle[j]
            if left_string not in record_super.keys():
                record_super[left_string] = [right_string]
            else:
                record_super[left_string].append(right_string)
            # l.append((left_string, right_string))
            if (left_string, right_string) not in encode:
                encode[(left_string, right_string)] = Bool(str(encode_index))
                encode_index += 1
            #propositional variable
            p = encode[(left_string, right_string)]
            # append the negotiation of this propositional variable
            clause = Or(clause, Not(p))
        o.add (clause)

for e in encode:
    o.add_soft(encode[e], 1)


# to the most one superclass

for l in record_super:
    clause = False
    for r in record_super[l]:
        clause = Or(clause, Not(encode[(l,r)]))
    o.add(clause)

# >>> element_by_symbol['H']
# 'hydrogen'
# >>> element_by_symbol.inverse['hydrogen']
# 'H'

print ('There are  in total ', count, ' cycles')
print ('There are in total ',  len (list(nodes)) ,' nodes involved')
print ('There are only ', len (encode), ' propositional variables')

# ===============
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time taken for encoding: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))



print(o.check())
# print(o.model())
m = o.model()

bidict_encode_decode = bidict(encode)


for e in encode:
    (left, right) = e
    left_index = int(left)
    right_index = int(right)

    left_name = hdt_lod.convert_id(left_index, IdentifierPosition.Subject)
    right_name = hdt_lod.convert_id(right_index, IdentifierPosition.Object)
    print ('left  = ', left_name)
    print ('right = ', right_name)
    print (e, 'assigns to' ,m.evaluate(encode[e]))
    if m.evaluate(encode[e]) == True:
        result_edges.append((left_index, right_index))
    print ('=================\n')

# ===============
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time taken for encoding + solving +decoding: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
# ===============



# G.add_edges_from(list(set(result_edges)))
#
# # values = [val_map.get(node, 0.25) for node in G.nodes()]
# pos = nx.spring_layout(G)
# nx.draw_networkx_labels(G, pos)
# # nx.draw(G, cmap = plt.get_cmap('jet'))
# nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
# plt.show()
#





# ===============
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time taken for encoding + solving + decoding + plotting: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
# ===============
