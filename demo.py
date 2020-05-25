# Shuai Wang
# VU Amsterdam
# DEMO for SUBMASSIVE 
from hdt import HDTDocument, IdentifierPosition
import sys
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import scipy
import tldextract

subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"

PATH_LOD = "./refined-subC-SA.hdt"
# PATH_LOD = "./subC-all.hdt"
hdt_file = HDTDocument(PATH_LOD)

query = ''
graph = nx.DiGraph()

def get_domain_and_label(t):
    domain = tldextract.extract(t).domain
    name1 = t.rsplit('/', 1)[-1]
    name2 = t.rsplit('#', 1)[-1]
    if len(name2) < len(name1):
        return (domain, name2)
    else:
        return (domain, name1)

def find_all_superclass():
    query_entity = query
    last_size = len(graph.edges)
    print ('entity = ', query_entity)
    # print ('cardi = ', cardinality)
    graph.add_node(query_entity)
    nodes = list(graph.nodes).copy()
    for n in nodes:
        triples, cardinality = hdt_file.search_triples(n, subClassOf, '')
        for (s, p, o) in triples:
            print ('subClassOf: ', o, '\n')
            graph.add_edge(s, o)
            # O.append(o)
        #do-while loop:
    while len(graph.edges) > last_size:
        last_size = len(graph.edges)
        nodes = list(graph.nodes).copy()
        for n in nodes:
            triples, cardinality = hdt_file.search_triples(n, subClassOf, '')
            for (s, p, o) in triples:
                print ('subClassOf: ', o, '\n')
                graph.add_edge(s, o)


def find_immediate_superclass():
    query_entity = query
    print ('entity = ', query_entity)
    triples, cardinality = hdt_file.search_triples(query_entity, subClassOf, '')
    print ('cardi = ', cardinality)
    O = []
    graph.add_node(query_entity)
    for (s, p, o) in triples:
        print ('subClassOf: ', o, '\n')
        graph.add_edge(query_entity, o)
        O.append(o)

    return O

def plot_graph(file_name='output'):
    pos = nx.kamada_kawai_layout(graph)
    # pos = nx.spring_layout(graph)
    # pos = nx.spectral_layout(graph)
    # pos = nx.spiral_layout(graph)
    nx.draw_networkx_nodes(graph, pos,
                           nodelist = graph.nodes,
                           node_color = 'g',
                           node_size=5,
                       alpha=0.8)

    nx.draw_networkx_nodes(graph, pos,
                           nodelist = [query],
                           node_color = 'b',
                           node_size=10,
                       alpha=0.8)

    nx.draw_networkx_edges(graph, pos,
                           edgelist=graph.edges,
                           width=1,alpha=0.5,edge_color='r')

    labels = {}
    for n in graph.nodes:
        (domain,name) = get_domain_and_label(n)
        labels[n] = domain + ':' + name
    nx.draw_networkx_labels(graph,pos,labels,font_size=5)

    plt.savefig(file_name + '.png')
    plt.savefig(file_name + '.svg')
    plt.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', action='store', required=True, help='enable the long listing formatxx')
    parser.add_argument('--plot', action='store_true', help='enable the long listing format')
    parser.add_argument('--all', action='store_true', help='enable the long listing format')

    args = parser.parse_args()
    # print(args.input)
    # print (args.i)
    #
    query = args.input
    if args.all == True:
        find_all_superclass()
    else:
        find_immediate_superclass()

    if args.plot == True:
        print ('also output the plot')
        plot_graph()
