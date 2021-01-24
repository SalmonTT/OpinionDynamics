import networkx as nx
import collections
from operator import itemgetter
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import community as community_louvain

'''
This file is to analyse networks, including:
    -   Basic information: max degrees, degree centrality, closeness centrality, betweenness centrality, eigenvector centrality
    -   Degree histogram
    -   Degree distribution
    -   Clustering coefficient
    -   Community analysis
'''

# G = some networkx graph

def networkAnalysis(G):
    basicInfo(G)
    degreeHistogram(G)
    degreeDistribution(G)
    clusteringCoefficient(G)

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
    top_degree_cen = get_top_keys(degree_cen, 5)
    print("The top 5 degree centrality are", list(top_degree_cen))
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
    plt.title('PA Model')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    # plt.savefig('./degree_distribution.pdf')
    plt.show()

def clusteringCoefficient(G):
    # Clustering coefficient of all nodes (in a dictionary)
    clust_coefficients = nx.clustering(G)
    # print("Cluster coefficients: ", clust_coefficients)
    ave_clust = nx.average_clustering(G)
    print("Average clustering coefficient of the graph: %.3f" % ave_clust)

def communityANalysis(G):
    partition = community_louvain.best_partition(G)
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count += 1.
        list_nodes = [nodes for nodes in partition.keys()
                       if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                                node_color=str(count / size))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()

def fullAnalysis(G):
    basicInfo(G)
    degreeHistogram(G)
    degreeDistribution(G)
    clusteringCoefficient(G)
    density = nx.density(G)
    print("Network density:", density)
    triadic_closure = nx.transitivity(G)
    print("Triadic closure:", triadic_closure)
    communityANalysis(G)
    shortestPath = nx.average_shortest_path_length(G)
    print("Average shortest path length: ", shortestPath)
    return

def csvAnalysis(filename):
    df = pd.read_csv(filename)
    pd.set_option('display.expand_frame_repr', False)

    # # analyze the convergence time
    # print("The summary of convergence time of graphs: ")
    # # find the mean, std, min, 25%, 50%, 75%, max
    # print(df[['Complete_time','Star_time', 'SW_time', 'ER_time', 'PA_time', 'L2_time']].describe())
    # # find the top 10 and last 10 in convergence time
    # top_10 = pd.DataFrame()
    # last_10 = pd.DataFrame()
    # for graph in 'Complete_time','Star_time', 'SW_time', 'ER_time', 'PA_time', 'L2_time':
    #     max = df.sort_values(graph, ascending=False).head(10)
    #     top_10[graph] = max[graph].tolist()
    #     min = df.sort_values(graph, ascending=True).head(10)
    #     last_10[graph] = min[graph].tolist()
    # print("The top ten are: ")
    # print(top_10)
    # print("the min ten are: ")
    # print(last_10)

    # distribution of convergence time type
    # print("The SW converge type distribution is ")
    # print(df['SW_timeType'].value_counts())
    # print("The ER converge type distribution is ")
    # print(df['ER_timeType'].value_counts())
    # print("The PA converge type distribution is ")
    # print(df['PA_timeType'].value_counts())
    # print("The L2 converge type distribution is ")
    # print(df['L2_timeType'].value_counts())

    # check the distribution of those reach stable distribution
    graphs = ['SW', 'ER', 'PA', 'L2']
    for graph in graphs:
        subgraph = df.loc[df[(graph+'_timeType')] == 1, (graph+'_opinion1')]
        # result = sum(1 for x in subgraph[2] if x>10 and x<90)
        print(subgraph)


    # df.hist(figsize=(20, 20))
    # plt.show()

# csvAnalysis(r'simulation result/LPA2_node100.csv')

def csvA(filename):
    df = pd.read_csv(filename)
    df = df.replace(20000, np.nan)
    pd.set_option('display.expand_frame_repr', False)
    print(df.describe(include='all'))
    top_10 = pd.DataFrame()
    last_10 = pd.DataFrame()
    # print(df.head(10))

    for graph in  list(df.columns):
        max = df.sort_values(graph, ascending=False).head(10)
        top_10[graph] = max[graph].tolist()
        min = df.sort_values(graph, ascending=True).head(10)
        last_10[graph] = min[graph].tolist()
    print("The top ten are: ")
    print(top_10)
    print("the min ten are: ")
    print(last_10)
    # df.hist(figsize=(20, 20))
    # plt.show()

# csvA('voter_3_10.csv')