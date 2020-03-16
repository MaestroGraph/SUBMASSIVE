import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from(
    [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
     ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

# val_map = {'A': 1.0,
#            'D': 0.5714285714285714,
#            'H': 0.0}

# values = [val_map.get(node, 0.25) for node in G.nodes()]
pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos)
# nx.draw(G, cmap = plt.get_cmap('jet'))
nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
plt.show()
