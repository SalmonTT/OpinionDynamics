# https://towardsdatascience.com/the-poisson-process-everything-you-need-to-know-322aa0ab9e9a
# voting models in random networks
from PA import *
from pyvis.network import Network
from scipy.stats import poisson
from numpy import random
import math
import collections


def interactiveGraphWithOpinion(G):
    # plot interactive graph using pyvis, with degree, no of node labeled, size depends on nodes' degree
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    nt.barnes_hut(spring_strength=0.006)
    for node in G:
        nt.add_node(node, label=G.degree(node), title="node " + str(node) + ' ' + str(G.nodes[node]['opinion']),
                    value=G.degree(node))

    for edge in G.edges:
        nt.add_edge(int(edge[0]), int(edge[1]), color='white')
    nt.show("nx.html")


def currentOpinion(G):
    count_pos = getPosOpinion(G)
    count_neg = nx.number_of_nodes(G) - count_pos
    print("The number of nodes with opinion 1 is %d. The number of nodes with opinion -1 is %d. " % (
    count_pos, count_neg))


def getPosOpinion(G):
    opin = nx.get_node_attributes(G, 'opinion')
    count_pos = 0
    for k, v in opin.items():
        if v == 1:
            count_pos = count_pos + 1
    return count_pos


def voterV1(max_nodes, num_updates):
    # step one: create a social network
    # graph = preferentialAttachmentV1(max_nodes)
    graph = barabasiAlbertGraph(100, 50)
    addFeature(graph)
    currentOpinion(graph)
    # step three: iterate through n number of updates
    for k in range(num_updates):
        # for each update k, update j number of nodes opinions via Poisson process with lamba=1 following voter algorithm
        # get a list of nodes that needs to be updated:
        # print(str(k) + " round" + " node 5 opinion: "+str(graph.nodes[5]['opinion']))
        p = poisson.pmf(1, 1)
        update_nodes = []
        all_nodes = list(range(max_nodes))
        for node in all_nodes:
            if np.random.uniform(0, 1) < p:
                update_nodes.append(node)
        for node in update_nodes:
            graph.nodes[node]['opinion'] = graph.nodes[random.choice([n for n in graph.neighbors(node)])]['opinion']

    # interactiveGraphWithOpinion(graph)
    currentOpinion(graph)
    return


def voterPiper(max_nodes, max_no_edge, poisson_lambda, process_time):
    G = barabasiAlbertGraph(max_nodes, max_no_edge)
    addFeature(G)
    currentOpinion(G)
    events = {}
    for node in G:
        n = random.random()
        inter_event_time = -math.log(1.0 - n) / poisson_lambda
        event_time = inter_event_time
        while event_time <= process_time:
            if event_time in events:
                events[event_time].append(node)
            else:
                events[event_time] = [node]
            n = random.random()
            inter_event_time = -math.log(1.0 - n) / poisson_lambda
            event_time = event_time + inter_event_time

    sorted_events = collections.OrderedDict(sorted(events.items()))
    no_ite = 0
    for time_t in sorted_events.keys():
        for node in sorted_events[time_t]:
            no_ite += 1
            G.nodes[node]['opinion'] = G.nodes[random.choice([n for n in G.neighbors(node)])]['opinion']
            print("At time %f, Node %d changed its opinion to %d. There are still %d has pos opinion" %
                  (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                currentOpinion(G)
                return

    currentOpinion(G)
    return


voterPiper(100, 50, 10, 10)

# G = barabasiAlbertGraph(100,50)
# addFeature(G)
# interactiveGraphWithOpinion(G)
