import random
import numpy as np
import networkx as nx
from plotGraph import plotGraph
from networkAnalysis import networkAnalysis
from PA import randomSubset

def completeGraph(no_node):
    return nx.complete_graph(no_node)

def starGraph(no_node):
    return nx.star_graph(no_node)

def cycleGraph(no_node):
    return nx.cycle_graph(no_node)

def lineGraph(no_node):
    return nx.path_graph(no_node)

def erdosRenyiGraph(no_node, p):
    return nx.fast_gnp_random_graph(no_node, p)

def barabasiAlbertGraph(no_node, max_no_edge, seed=None):
    G = nx.empty_graph(2)
    targets = list(range(2))
    repeated_nodes = []
    source = 2
    no_edge = random.randint(1,2)
    while source < no_node :
        G.add_edges_from(zip([source]*no_edge, targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source]*no_edge)
        no_edge = random.randint(1, min(max_no_edge, nx.number_of_nodes(G)))
        targets = randomSubset(repeated_nodes, no_edge)
        source += 1
    # networkAnalysis(G)
    # plotGraph(G)
    return G

# barabasiAlbertGraph(80, 3, seed=None)

def preferentialAttachment_2ndOrder(max_nodes, c=1.0, loner=False):
    G = nx.Graph()
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    for i in range(2, max_nodes):
        existing_node_list = sorted(G.degree, key=lambda x: x[1], reverse=True)
        G.add_node(i)
        for node, degrees in existing_node_list:
            sum_neighbors_degree = 0
            sum_neighbors_degree_squared = 0
            for neighbor in G.neighbors(node):
                sum_neighbors_degree += G.degree(neighbor)
                sum_neighbors_degree_squared += pow(G.degree(neighbor), 2)
            p = (G.degree(node) + c * sum_neighbors_degree) / (
                        2 * G.number_of_edges() + c * sum_neighbors_degree_squared)
            if random.random() <= p:
                G.add_edge(node, i)
        if not loner and G.degree(i) == 0:
            rand_node = np.random.randint(0, i - 1)
            G.add_edge(rand_node, i)

    # networkAnalysis(G)
    # plotGraph(G)
    return G

# preferentialAttachment_2ndOrder(80, c=0.5)