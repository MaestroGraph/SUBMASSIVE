# evaluate the automatically removed edges - 330
import networkx as nx
import sys
import csv
import time
from collections import Counter
import tldextract
import json


auto_file_name = 'final_removed_edges_60:11_330_00:30:25.04.csv'
auto_file_name_csv = open (auto_file_name, newline='')
auto_file_name_csv_reader = csv.DictReader(auto_file_name_csv)
auto = []
for row in auto_file_name_csv_reader:
    s = row['SUBJECT']
    o = row['OBJECT']
    auto.append((s, o))


manual_file_name = 'lod-two-cycle.csv'
manual_file_name_csv = open (manual_file_name, newline='')
manual_file_name_csv_reader = csv.DictReader(manual_file_name_csv)
manual = []
manual_remain = []
manual_unknown = []
for row in manual_file_name_csv_reader:
    s = row['SUBJECT']
    o = row['OBJECT']
    if row['SUGGESTION'] == 'remove':
        manual.append((s, o))
    if row['SUGGESTION'] == 'remain':
        manual_remain.append((s,0))
    if row['DECISION'] == 'u':
        manual_unknown.append((s,o))


manual_auto_file_name = 'final_removed_edges60.csv'
manual_auto_file_name_csv = open (manual_auto_file_name, newline='')
manual_auto_file_name_csv_reader = csv.DictReader(manual_auto_file_name_csv)
manual_auto = []
for row in manual_auto_file_name_csv_reader:
    s = row['SUBJECT']
    o = row['OBJECT']
    # if row['SUGGESTION'] == 'remove':
    manual_auto.append((s, o))


print ('there are ', len(auto), ' removed relations in auto' )
print ('there are ', len(manual), ' removed relations in manual' )
print ('there are ', len(manual_auto), ' removed relations in manual_auto' )



common_list_auto_manual = [value for value in manual if value in auto]
print ('there are ', len (common_list_auto_manual),  ' entries in both manual decision and auto')


common_list_auto_manual = [value for value in manual_auto if value in auto]
print ('there are ', len (common_list_auto_manual),  ' entries in both manual_auto and auto')

print ('remain===', len(manual_remain))
# manual_remain
against_list_auto_and_manual = [value for value in manual_remain if value in auto]
print ('there are ', len (against_list_auto_and_manual),  ' entries in auto but suggested remain in manual')

print('unknown===', len(manual_unknown))
against_list_auto_and_manual_unknown = [value for value in manual_unknown if value in auto]

print ('*there are ', len (against_list_auto_and_manual_unknown),  ' entries in auto but UNKNOWN in manual')
