# this script is to print the opencyc



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



# What are these OpenCyc about
visited_pair_list = []
hdt_file = None
output_filename = None
# if sys.argv [1] == 'lod':
hdt_file = HDTDocument(PATH_LOD)
output_filename = 'lod-two-cycle.csv'

# Predicates :


predicate_names = [
"http://sw.cyc.com/CycAnnotations_v1#label",
"http://www.w3.org/2000/01/rdf-schema#comment",
"http://www.w3.org/2000/01/rdf-schema#label"
]

names = ["http://sw.opencyc.org/2008/06/10/concept/Mx4rHDx7kEAbEdqAAAACs0uFOQ",
"http://sw.opencyc.org/2008/06/10/concept/Mx4rvpDCHZwpEbGdrcN5Y29ycA",
"http://sw.opencyc.org/concept/Mx4rvtUAU5wpEbGdrcN5Y29ycA",
"http://sw.opencyc.org/concept/Mx8Ngh4rvmtxnJwpEbGdrcN5Y29ycB4rvViA9JwpEbGdrcN5Y29ycA"
]
