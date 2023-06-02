import urllib.request

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import gzip

# آدرس فایل دانلود
url = "http://snap.stanford.edu/data/soc-Epinions1.txt.gz"
file_name = "soc-Epinions1.txt.gz"

# دانلود فایل
urllib.request.urlretrieve(url, file_name)

# استخراج فایل فشرده
with gzip.open(file_name, "rb") as f_in:
    with open("soc-Epinions1.txt", "wb") as f_out:
        f_out.write(f_in.read())

# بارگیری مجموعه داده با استفاده از NetworkX
G = nx.read_edgelist("soc-Epinions1.txt", create_using=nx.DiGraph(), nodetype=int)

# -------------------------------------------
# -------------------------------------------
# 1 Number of nodes
# 2 Number of edges
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print("Number of nodes:", num_nodes)
print("Number of edges:", num_edges)
# -------------------------------------------
# -------------------------------------------
# 22 Compute the in-degree and out-degree distributions and plot the power law for
# each of these distributions
# # Compute the in-degree distribution
in_degrees = dict(G.in_degree())
in_degree_values = np.array(list(in_degrees.values()))
in_degree_hist, in_degree_bins = np.histogram(in_degree_values, bins='auto', density=True)

# Compute the out-degree distribution
out_degrees = dict(G.out_degree())
out_degree_values = np.array(list(out_degrees.values()))
out_degree_hist, out_degree_bins = np.histogram(out_degree_values, bins='auto', density=True)

# Plot the power law for in-degree distribution
in_degree_logbins = np.logspace(np.log10(np.min(in_degree_values[in_degree_values > 0])),
                                np.log10(np.max(in_degree_values)), num=len(in_degree_bins))
in_degree_loghist = np.histogram(in_degree_values, bins=in_degree_logbins, density=True)[0]
plt.loglog(in_degree_logbins[:-1], in_degree_loghist, 'b-', marker='o', markersize=3, label='In-degree')

# Plot the power law for out-degree distribution
out_degree_logbins = np.logspace(np.log10(np.min(out_degree_values[out_degree_values > 0])),
                                 np.log10(np.max(out_degree_values)), num=len(out_degree_bins))
out_degree_loghist = np.histogram(out_degree_values, bins=out_degree_logbins, density=True)[0]
plt.loglog(out_degree_logbins[:-1], out_degree_loghist, 'r-', marker='o', markersize=3, label='Out-degree')

# Set plot labels and legend
plt.xlabel('Degree')
plt.ylabel('Probability Density')
plt.legend()

# Show the plot
plt.show()
# -------------------------------------------
# -------------------------------------------
# 23 Choose 100 nodes at random from the network and do one forward and one backward BFS traversal for each node. Plot the cumulative distributions of the nodes covered in these BFS runs as  Create one figure for the forward BFS and one for the backward BFS. How many nodes are in the OUT and IN components?
# How many nodes are in the TENDRILS component?
# (Hint: The forward BFS plot gives the number of nodes in SCC+OUT and similarly, the backward BFS plot gives the number of nodes in SCC+IN
# Choose 100 random nodes
random_nodes = random.choices(list(G.nodes()), k=1)

forward_nodes_covered = []
backward_nodes_covered = []

for node in random_nodes:
    # Perform forward BFS
    forward_bfs = nx.bfs_successors(G, node)
    forward_nodes = [node] + [v for sublist in forward_bfs for v in sublist]
    forward_nodes_covered = sorted(map(int, forward_nodes_covered), reverse=True)

    # Perform backward BFS
    backward_bfs = nx.bfs_predecessors(G.reverse(), node)
    backward_nodes = [node] + [v for v, _ in backward_bfs]
    backward_nodes_covered.extend(backward_nodes)

# Calculate cumulative distributions
forward_cumulative = np.arange(len(forward_nodes_covered)) + 1
backward_cumulative = np.arange(len(backward_nodes_covered)) + 1

# Plot cumulative distributions
plt.plot(sorted(forward_nodes_covered, reverse=True), forward_cumulative, label='Forward BFS')
plt.plot(sorted(backward_nodes_covered, reverse=True), backward_cumulative, label='Backward BFS')
plt.xlabel('Number of Nodes Covered')
plt.ylabel('Cumulative Distribution')
plt.legend()
plt.show()

# Calculate the number of nodes in OUT, IN, and TENDRILS components
out_component_nodes = len(set(forward_nodes_covered))
in_component_nodes = len(set(backward_nodes_covered))
tendrils_component_nodes = len(G.nodes()) - out_component_nodes - in_component_nodes

print("Number of nodes in OUT component:", out_component_nodes)
print("Number of nodes in IN component:", in_component_nodes)
print("Number of nodes in TENDRILS component:", tendrils_component_nodes)
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# 24 What is the probability that a path exists between two nodes chosen uniformly
# from the graph? What if the node pairs are only drawn from the WCC of the two
# networks? Compute the percentage of node pairs that were connected in each of
# these cases
# Compute the probability of a path between two uniformly chosen nodes
def compute_path_probability(G):
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    node1, node2 = random.sample(nodes, 2)
    if nx.has_path(G, node1, node2):
        return 1.0 / (num_nodes * (num_nodes - 1))
    else:
        return 0.0

# Compute the probability of a path between two uniformly chosen nodes from the WCC
def compute_wcc_path_probability(G):
    wcc = max(nx.weakly_connected_components(G), key=len)
    wcc_nodes = list(wcc)
    num_wcc_nodes = len(wcc_nodes)
    node1, node2 = random.sample(wcc_nodes, 2)
    if nx.has_path(G, node1, node2):
        return 1.0 / (num_wcc_nodes * (num_wcc_nodes - 1))
    else:
        return 0.0

# Number of iterations to compute the probabilities
num_iterations = 1

# Calculate the probability of a path and the percentage of connected node pairs for each case
total_path_probability = 0.0
total_wcc_path_probability = 0.0
connected_pairs_percentage = 0.0
wcc_connected_pairs_percentage = 0.0

for _ in range(num_iterations):
    path_probability = compute_path_probability(G)
    wcc_path_probability = compute_wcc_path_probability(G)
    total_path_probability += path_probability
    total_wcc_path_probability += wcc_path_probability
    if path_probability > 0.0:
        connected_pairs_percentage += 1
    if wcc_path_probability > 0.0:
        wcc_connected_pairs_percentage += 1

connected_pairs_percentage /= num_iterations
wcc_connected_pairs_percentage /= num_iterations

print("Probability of a path between two uniformly chosen nodes:", total_path_probability)
print("Percentage of connected node pairs (all nodes):", connected_pairs_percentage * 100)
print("Probability of a path between two uniformly chosen nodes from the WCC:", total_wcc_path_probability)
print("Percentage of connected node pairs (WCC only):", wcc_connected_pairs_percentage * 100)
