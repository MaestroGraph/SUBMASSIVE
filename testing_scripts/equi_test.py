# test equivalent class


import csv
from bidict import bidict
# file_name = "id2terms_0-99_10000.csv"
# file_name = "term2id_0-99.csv"

# file = open(file_name,'r' ,newline='')
# reader = csv.DictReader(file)
# for row in reader:
#     for key, value in row.items():
#         print ('key  :', key)
#         print ('value:', value)
#

#
# with open(file_name, 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#
#     output_filename = "term2id.csv"
#     file2 = open(output_filename, 'w', newline='')
#     writer = csv.writer(file2)
#     writer.writerow([ "TERM", "GROUPID"])
#
#     for row in reader:
#         # print ('original row = ', row)
#         # print ('row length   = ', len(row))
#         term = ''
#         if len(row) > 2:
#             term = row[0]+row[1]
#         else:
#             term = row[0]
#         # print ('term = ', term)
#         term = term.split('^^')
#         # print ('tmp = ', term)
#         term = term[0][1:-1]
#         id = int(row[-1])
#     # if len(row) != 2:
#         # print ('original row = ', row)
#         # print ('term = ', term)
#         # print ('group_id   = ', id)
#         # print ('\n\n')
#         writer.writerow([term, id])

#
#
# import csv
# import re
# # file_name = "id2terms_0-99_10000.csv"
# file_name = "term2id_0-99_1000.csv"
#
# file = open(file_name,'r' ,newline='')
# f = file.readlines()
#
# output_filename = "term2id.csv"
# file2 = open(output_filename, 'w', newline='')
# writer = csv.writer(file2)
# writer.writerow([ "TERM", "ID"])
#
#
# for l in f:
#     left = l.find('<')
#     right = l.find('>')
#     if left != -1 and right != -1:
#         left-=2
#         right +=2
#         # print ()
#         term = l[:left][1:-1]
#         id = int(l[right:])
#         writer.writerow([term, id])

# the last test from last year
# file_name = "term2id.csv"
# with open(file_name, 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print ('term   :', row["TERM"])
#         print ('groupid:', row["GROUPID"])


# from Joe's Email :

# file_name = "term2id_0-99.csv"
file_name = "term2id_0-99_1000.csv"
#
def splitTermAndID(line):
    parts = line.split(" ")
    if len(parts) ==2:
        return parts
    else:
        # when an element contains an empty space
        term = ""
        for i in range(len(parts) - 1):
            term = term + parts[i]
        return [term, parts[-1]]

with open(file_name) as f:
    line = f.readline()
    cnt = 0
    while line:
        splitted_line = splitTermAndID(line)
        # values
        value = splitted_line[1]
        # key
        key = splitted_line[0]
        key = key.split('^^')
        key = key[0][1:-1]
        print(key, value)
        line = f.readline()
        cnt += 1
    print("DONE! Finished reading file TERM2ID. There is a total of ", "{:,}".format(cnt), "terms")

# create a bidirectional dictionary

element_by_symbol = bidict({'H': 'hydrogen'})
element_by_symbol['H'] = 'jack'
print (element_by_symbol['H'])
# print (element_by_symbol.inverse['hydrogen'])
