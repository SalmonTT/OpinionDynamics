# https://towardsdatascience.com/the-poisson-process-everything-you-need-to-know-322aa0ab9e9a
# voting models in random networks
from PA import *
from pyvis.network import Network
from scipy.stats import poisson
import numpy as np
import math
import collections
import pandas as pd


# Add attributes to nodes in G
def addFeature(G, num):
    stubborn_agents = random.sample(list(G), num)
    for node in G:
        init_opinion = np.random.choice([-1, 1])
        G.nodes[node]['opinion']=init_opinion
        if node in stubborn_agents:
            G.nodes[node]['stubborness'] = 1
        else:
            G.nodes[node]['stubborness'] = 0
    return G

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


def getCurrentOpinion(G):
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


def voterModelStubborn(max_nodes, max_edges, num_updates, process_time, num_stubborn):
    # Stubborn agents are individuals are thought to be continuously influencing their
    # neighbors via original voter model update rules, but never update their decisions (opinions)
    # Note that while the paper uses a directed graph, we will use an undirected graph here
    G = barabasiAlbertGraph(max_nodes, max_edges)
    addFeature(G, num_stubborn)
    getCurrentOpinion(G)
    schedule = {}
    for node in G:
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= process_time:
                if arrival_time in schedule:
                    schedule[arrival_time].append(node)
                else:
                    schedule[arrival_time] = [node]
            else:
                break

    sorted_schedule = collections.OrderedDict(sorted(schedule.items()))
    print(sorted_schedule)
    update_count = 0
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                getCurrentOpinion(G)
            update_count += 1
            if update_count >= num_updates:
                getCurrentOpinion(G)
                return

    getCurrentOpinion(G)
    return

def voterModel(max_nodes, max_edges, num_updates, process_time):
    # num_updates is the total number of updates that will occur
    # process_time is the length of the poisson process for each agent/node
    G = barabasiAlbertGraph(max_nodes, max_edges)
    addFeature(G,0)
    getCurrentOpinion(G)
    # key = update time, value = update node
    schedule = {}
    for node in G:
        # arrival_time is the arrival time for ith update
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= process_time:
                if arrival_time in schedule:
                    schedule[arrival_time].append(node)
                else:
                    schedule[arrival_time] = [node]
            else: break

    sorted_schedule = collections.OrderedDict(sorted(schedule.items()))
    print(sorted_schedule)
    update_count = 0
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                getCurrentOpinion(G)
            update_count+=1
            if update_count >= num_updates:
                getCurrentOpinion(G)
                return

    getCurrentOpinion(G)
    return

def voterPiper(max_nodes, max_no_edge, poisson_lambda, discrete_process_time):
    G = barabasiAlbertGraph(max_nodes, max_no_edge)
    addFeature(G,0)
    getCurrentOpinion(G)
    events = {}
    for node in G:
        n = random.random()
        inter_arrival_time = -math.log(1.0 - n) / poisson_lambda
        event_time = inter_arrival_time
        while event_time <= discrete_process_time:
            if event_time in events:
                events[event_time].append(node)
            else:
                events[event_time] = [node]
            n = random.random()
            inter_arrival_time = -math.log(1.0 - n) / poisson_lambda
            event_time = event_time + inter_arrival_time

    sorted_events = collections.OrderedDict(sorted(events.items()))
    print(sorted_events)
    no_ite = 0
    for time_t in sorted_events.keys():
        for node in sorted_events[time_t]:
            no_ite += 1
            G.nodes[node]['opinion'] = G.nodes[random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                getCurrentOpinion(G)
                return

    getCurrentOpinion(G)
    return


voterModelStubborn(100, 50, 6000, 50, 10)

# voterModel(100, 50, 6000, 50)