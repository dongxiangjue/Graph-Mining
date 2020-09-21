import csv
import networkx as nx
from pyvis.network import Network
import community
from operator import itemgetter
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

with open('quakers_nodelist.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    nodes = [i for i in reader][1:]

# print(nodes)
node_names = [i[0] for i in nodes]

with open('quakers_edgelist.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    edges = [tuple(i) for i in reader][1:]

# print(edges)
print(len(nodes))
print(len(edges))

# initialize a Graph object
G = nx.Graph()
# add nodes and edges
G.add_nodes_from(node_names)
G.add_edges_from(edges)
print(nx.info(G))

history = {}
gender = {}
birth = {}
death = {}
id = {}

for node in nodes:
    history[node[0]] = node[1]
    gender[node[0]] = node[2]
    birth[node[0]] = node[3]
    death[node[0]] = node[4]
    id[node[0]] = node[5]

# add six attributes
nx.set_node_attributes(G, history, 'historical_significance')
nx.set_node_attributes(G, gender, 'gender')
nx.set_node_attributes(G, birth, 'birthdate')
nx.set_node_attributes(G, death, 'deathdate')
nx.set_node_attributes(G, id, 'id')

density = nx.density(G)
print("Network density:", density)

fell_whitehead_path = nx.shortest_path(G, source="Margaret Fell", target="George Whitehead")

print("Shortest path between Fell and Whitehead:", fell_whitehead_path)
print("Length of that path:", len(fell_whitehead_path)-1)
# for n in G.nodes():
#     print(n, G.nodes[n]['birthdate'])

print(nx.is_connected(G))
components = nx.connected_components(G)
largest_component = max(components, key=len)

subgraph = G.subgraph(largest_component)
diameter = nx.diameter(subgraph)
print("Network diameter of largest component:", diameter)

triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)

degree_dict = dict(G.degree(G.nodes()))
print(degree_dict)
nx.set_node_attributes(G, degree_dict, 'degree')
print(G.nodes['William Penn'])
sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
print("Top 5 nodes by degree:")
for d in sorted_degree[:5]:
    print(d)
eigenvector_dict = nx.eigenvector_centrality(G)
betweenness_dict = nx.betweenness_centrality(G)

nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')
nx.set_node_attributes(G, betweenness_dict, 'betweenness')

sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)

print("Top 5 nodes by betweenness centrality:")
for b in sorted_betweenness[:5]:
    print(b)

top_betweenness = sorted_betweenness[:20]

for tb in top_betweenness:
    degree = degree_dict[tb[0]]
    print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)

sorted_eigenvector = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)

print("Top 5 nodes by eigenvector centrality:")
for b in sorted_eigenvector[:5]:
    print(b)

communities = community.best_partition(G)
print(communities)
global_modularity = community.modularity(communities, G)
print("global_modularity", global_modularity)

# def simple_update(num, n, layout, G, ax):
#     ax.clear()
#
#     # Draw the graph with random node colors
#     random_colors = np.random.randint(2, size=n)
#     nx.draw(G, pos=layout, node_color=random_colors, ax=ax)
#
#     # Set the title
#     ax.set_title("Frame {}".format(num))
#
#
# def simple_animation(G, nodes, edges):
#
#     # Build plot
#     fig, ax = plt.subplots(figsize=(6,4))
#
#     # Create a graph and layout
#     n = len(nodes) # Number of nodes
#     m = len(edges) # Number of edges
#     layout = nx.spring_layout(G)
#
#     ani = animation.FuncAnimation(fig, simple_update, frames=10, fargs=(n, layout, G, ax))
#     ani.save('animation_1.gif', writer='imagemagick')
#
#     plt.show()
#
# simple_animation(G, nodes, edges)

# communities = community.greedy_modularity_communities(G)
# modularity = {}
# for i,c in enumerate(communities):
#     print(i)
#     for name in c:
#         modularity[name] = i

# nx.set_node_attributes(G, modularity, 'modularity')

# Graph visualization
nt = Network("2500px", "2500px")
nt.from_nx(G)
nt.show("nx.html")