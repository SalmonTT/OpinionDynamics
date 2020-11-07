import random
import numpy as np
import networkx as nx
from plotGraph import *

def netwrokxBApreferentialAttachment(max_nodes, no_edges):
    G = nx.barabasi_albert_graph(max_nodes, no_edges)
    plotGraph(G)
    networkAnalysis(G)
    return (G)



def preferentialAttachmentV1(max_nodes, loner=False):
    G = nx.Graph()
    G.add_node(0, opinion=-1)
    G.add_node(1, opinion=1)
    G.add_edge(0, 1)
    p = 0.5
    # ----- Part 1 -----
    for i in range(2, max_nodes):
        # ----- Part 1.1 -----
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        init_opinion = random.choice([-1, 1])
        G.add_node(i, opinion=init_opinion)
        # ----- Part 1.2 -----
        for j in node_list:
            if G.number_of_edges() != 0:
                p = G.degree(j) / (2 * G.number_of_edges())
            if (round(np.random.uniform(0, 1), 1) < p):
                G.add_edge(j, i)
        # ----- Part 1.3 -----
        if not loner & (G.degree[i] == 0):
            # rand_node = node_list[random.choice(node_list)]
            # rand_node = node_list[0]
            # G.add_edge(rand_node, i)
            while(G.degree[i] == 0):
                for j in node_list:
                    if G.number_of_edges() != 0:
                        p = G.degree(j) / (2 * G.number_of_edges())
                    if (round(np.random.uniform(0, 1), 1) < p):
                        G.add_edge(j, i)

    # plotGraph(G)
    # networkAnalysis(G)
    return (G)



def preferentialAttachmentV2(max_nodes, loner=False, max_p=1.0):
    G = nx.Graph()
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    # ----- Part 1 -----
    for i in range(2, max_nodes):
        # ----- Part 1.1 -----
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        G.add_node(i)
        # ----- Part 1.2 -----
        for j in node_list:
            if (G.degree(j) / (2 * G.number_of_edges())) >= max_p:
                p = max_p
            else:
                p = G.degree(j) / (2 * G.number_of_edges())
            if random.random() <= p:
                G.add_edge(j, i)
        # ----- Part 1.3 -----
        if not loner & (G.degree(i) == 0):
            rand_node = node_list[random.choice(node_list)]
            G.add_edge(rand_node, i)

    networkAnalysis(G)
    plotGraph(G)
    return(G)

def preferentialAttachmentV3(max_nodes, loner=False):
    G = nx.Graph()
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    # ----- Part 1 -----
    for i in range(2, max_nodes):
        # ----- Part 1.1 -----
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        G.add_node(i)
        # ----- Part 1.2 -----
        count = max_nodes
        for j in node_list:
            p = G.degree(j) / (2 * G.number_of_edges())
            p = p + p * (1 - (1/(count+1)))
            if random.random() <= p:
                G.add_edge(j, i)
            count -= 1
        # ----- Part 1.3 -----
        if not loner & (G.degree(i) == 0):
            rand_node = node_list[random.choice(node_list)]
            G.add_edge(rand_node, i)

    networkAnalysis(G)
    plotGraph(G)
    return(G)


def preferentialAttachmentART(max_nodes = 100, loner=False, p_multi=2.0):
    G = nx.Graph()
    G.add_nodes_from([0, 1])
    G.add_edge(0, 1)
    # ----- Part 1 -----
    for i in range(2, max_nodes):
        # ----- Part 1.1 -----
        node_list = sorted(node for (node, val) in sorted(G.degree, key=lambda x: x[1], reverse=True))
        G.add_node(i)
        # ----- Part 1.2 -----
        count = 0
        for j in node_list:
            p = G.degree(j) / (2 * G.number_of_edges())
            p = p + p_multi * (1 - (1/(count+1)))
            if random.random() <= p:
                G.add_edge(j, i)
            count += 1
        # ----- Part 1.3 -----
        if not loner & (G.degree(i) == 0):
            rand_node = node_list[random.choice(node_list)]
            G.add_edge(rand_node, i)

    networkAnalysis(G)
    plotGraph(G)
    return(G)



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

            # print('did not form edge with prev. nodes, will add %d to rand. node %d' % (i, rand_node))
        # nx.draw(G, with_labels=True)
        # plt.show()
    networkAnalysis(G)
    plotGraph(G)
    return []



def preferentialAttachment_MDApseudo(max_nodes, m0, m):
    G = preferentialAttachmentV2(m0, 100)
    for new_node in range(m0 + 1, max_nodes):
        connected_nodes_list = []
        for n in G.degree:
            if n[1] != 0: connected_nodes_list.append(n[0])
        G.add_node(new_node)
        mediator = random.choice(connected_nodes_list)
        all_neighbors_list = list(G.neighbors(mediator))
        m_neighbors_list = []
        for n in range(min(m, G.degree(mediator))):
            neighbor = random.choice(all_neighbors_list)
            all_neighbors_list.remove(neighbor)
            m_neighbors_list.append(neighbor)
        for n in m_neighbors_list:
            G.add_edge(n, new_node)
            print('edge between %d and %d created' % (n, new_node))
        # nx.draw(G, with_labels=True)
        # plt.show()
    networkAnalysis(G)
    plotGraph(G)
    return []

def nonLinear(no_node, no_edge):
    # We can consider the probability of a new node (n+1) connected to a existing node u is
    # f(degree of m at time t)/n
    # If f(k) = b, there is no preferential attachment. (Constant case β=0)
    # If f(k) = ak + b, is the linear preferential attachment. (Linear caseβ=1)
    # To build a non-linear, we have f(k) = k^β
    # Sublinear case 0 < β < 1.
    # Superlinear case β > 1.
    pass

def randomSubset(repeated_nodes, no_edge):
    targets = set()
    while len(targets) < no_edge:
        x = random.choice(repeated_nodes)
        targets.add(x)
    return targets

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

# Add attributes to nodes in G
def addFeature(G):
    for node in G:
        init_opinion = random.choice([-1, 1])
        G.nodes[node]['opinion']=init_opinion
    return G

def plotPAgraph():
    # preferentialAttachment_2ndOrder(100, loner=False)
    netwrokxBApreferentialAttachment(100, 5)
    # preferentialAttachmentV1(100, loner=False)
    return


def preferentialAttachment_MDA(max_nodes, m0, m):
    # https://www.sciencedirect.com/science/article/pii/S0378437116308056?via%3Dihub
    G = preferentialAttachmentV1(m0)
    connected_nodes_list = []
    for new_node in range(m0 + 1, max_nodes):
        if new_node == m0+1:
            connected_nodes_list = list(G)
        G.add_node(new_node)
        m_count = 0
        while m_count < m:
            N = len(G)
            sum_inverse_degree = sum([1/G.degree[x] for x in G.neighbors(connected_nodes_list[m_count])])
            p = (1 / N) * sum_inverse_degree
            if random.random() <= p:
                G.add_edge(new_node, connected_nodes_list[m_count])
                m += 1
        connected_nodes_list.append(new_node)
    return G


barabasiAlbertGraph(100, 5)

