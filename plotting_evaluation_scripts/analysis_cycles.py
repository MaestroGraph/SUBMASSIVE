# analysis cycles
#
from hdt import HDTDocument, IdentifierPosition
import networkx as nx
import sys
import csv
import time
from collections import Counter
import tldextract
import json



def obtain_statistics (file_name):
    ct = Counter ()
    cross_domain = 0
    with open (file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            # print ('term: ', row['SUBJECT'])
            # print ('term: ', row['OBJECT'])
            # print ('sugg: ', row['SUGGESTION'])
            if row['SUGGESTION'] == 'remove':
                s_domain = tldextract.extract(row['SUBJECT']).domain
                o_domain = tldextract.extract(row['OBJECT']).domain
                if (s_domain != o_domain):
                    print ('\t\t\t\tsubj = ', row['SUBJECT'])
                    print ('\t\t\t\t obj = ', row['OBJECT'])
                    cross_domain += 1
                ct [s_domain] += 1
                ct [o_domain] += 1
                count += 1
        print ('There are ', count, ' No. of removed edges.')

    print ('There are ', cross_domain, ' cross-domain edges removed ')

    for c in ct.keys():
        ct[c] = ct[c]/2
    print('COUNT = ', ct)

    for c in ct.keys():
        ct[c] = ct[c]/2/count
    return ct


if __name__ == "__main__":
    # ct = obtain_statistics('final_removed_edges60.csv')
    # ct = obtain_statistics('lod-two-cycle.csv')
    # ct = obtain_statistics('equivalent-unnecessary-relations.csv')
    ct = obtain_statistics('final_removed_edges_60:11_330_00:30:25.04.csv')
    # ct = obtain_statistics('reflexive.csv')
    print (ct)

#
# cycles = []
# csv_filename = 'other_cycles.csv'
# reduced = open(csv_filename, newline='')
# reader = csv.DictReader(reduced)
#
#
#
# ct = Counter ()
# PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
# hdt_lod = HDTDocument(PATH_LOD)
# hdt_file = hdt_lod
#
# count = 0
# counter = Counter()
#
# with open('other_cycles.json', newline='') as f:
#     data = json.load(f)
#     for cycle in data:
#         count += 1
#         for c in cycle:
#             e_uri = hdt_file.convert_id(int(c), IdentifierPosition.Subject)
#             domain = tldextract.extract(e_uri).domain
#             ct [domain] += 1
#             counter[e_uri] +=1
#
# print ('There are  in total ', count, ' cycles')
# print ('There are in total ',  len (list(counter)) ,' nodes involved')
# # display the most common ten domains
# for (e,count) in ct.items():
#     print (e, ' has ', count)
#
# print ('=========')
# print (counter)
