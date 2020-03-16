import json
import networkx as nx

# v1 = ['jack', 'duck', 'lost']
# v2 = ['jack', 'duck', 'lost', 'me']
# v3 = [ 'duck', 'lost']
#
# some_list = [v1,v2,v3]
#
# outputfilename = 'list.output'
# with open(outputfilename, 'wb') as outfile:
#     json.dump(some_list, outfile)

# my_list = [ ['jack', 'big'], ['b'], ['c']]
# # my_json_string = json.dumps(my_list)
#
#
# with open('person.json', 'w+') as json_file:
#   json.dump(my_list, json_file)
#
# with open('person.json') as f:
#   data = json.load(f)
#   for d in data:
#       print (d)


G = nx.DiGraph([(1, 2), (2, 3), (3, 7), (7, 8), (8, 1), (4, 5), (5, 4),(3,8),(8,7), (7,6), (6,5), (5,3), (3,5), (6,3), (5,7)])
for c in list(nx.simple_cycles(G)):
    for node in c:
        print (node, ' \\rightarrow')

    print ('\n')
