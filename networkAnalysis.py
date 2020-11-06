import networkx as nx
import collections
from operator import itemgetter
import matplotlib.pyplot as plt
import json

# G = some networkx graph

def networkAnalysis(G):
    basicInfo(G)
    # degreeHistogram(G)
    # degreeDistribution(G)
    # clusteringCoefficient(G)



def get_top_keys(dictionary, top):
    items = sorted(dictionary.items(), reverse=True, key=lambda x: x[1])
    return map(lambda x: x[0], items[:top])

def basicInfo(G):
    n, e = G.number_of_nodes(), G.number_of_edges()
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    dmax = max(degree_sequence)
    print("Nodes: %d. Edges: %d. Max_degree: %d" % (n, e, dmax))

    # Degree Centrality of a node refers to the number of edges attached to the node.
    # The degree centrality values are normalized by dividing by the maximum possible
    # degree in a simple graph n-1 where n is the number of nodes in G.
    degree_cen = nx.degree_centrality(G)
    top_degree_cen = get_top_keys(degree_cen, 10)
    print("The top ten degree centrality are", list(top_degree_cen))

    # Closeness centrality of a node u is the reciprocal of the average shortest path
    # distance to u over all n-1 reachable nodes.
    #                          n - 1
    # Defined as C(u) = ----------------------
    #                    Σv=1->(n-1)  d(v,u)
    close_cen = nx.closeness_centrality(G)
    top_close_cen = get_top_keys(close_cen, 10)
    # print(json.dumps(close_cen, indent=4))
    print("The top ten closeness centrality are", list(top_close_cen))

    # Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v
    between_cen = nx.betweenness_centrality(G)
    top_between_cen = get_top_keys(between_cen,10)
    # print(json.dumps(between_cen, indent=4))
    print("The top ten betweenness centrality are", list(top_between_cen))

    # Eigenvector Centrality measures the importance of a node in a graph as a function of the
    # importance of its neighbors.
    # If a node is connected to highly important nodes, it will have a higher Eigen Vector
    # Centrality score as compared to a node which is connected to lesser important nodes.
    eigen_cen = nx.eigenvector_centrality(G)
    top_eigen_cen = get_top_keys(eigen_cen, 10)
    # print(json.dumps(eigen_cen, indent=4))
    print("The top ten eigenvector centrality are", list(top_eigen_cen))


def degreeHistogram(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.show()

def degreeDistribution(G):
    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    plt.figure()
    plt.grid(True)
    plt.loglog(degrees[:], degree_freq[:], 'go-')
    plt.title('Social Network')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    # plt.savefig('./degree_distribution.pdf')
    plt.show()

def clusteringCoefficient(G):
    # Clustering coefficient of all nodes (in a dictionary)
    clust_coefficients = nx.clustering(G)
    ave_clust = nx.average_clustering(G)
    print("Average clustering coefficient of the graph: %d" % ave_clust)

def fullAnalysis(G):
    basicInfo(G)
    degreeHistogram(G)
    degreeDistribution(G)
    clusteringCoefficient(G)
    return
