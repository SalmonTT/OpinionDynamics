# https://towardsdatascience.com/the-poisson-process-everything-you-need-to-know-322aa0ab9e9a
# voting models in random networks
from PA import *
from pyvis.network import Network
# from scipy.stats import poisson
import numpy as np
import math
import collections
import pandas as pd
from buildGraph import *

'''
This file is the early stage of voter model, including binary & multiple opinions
'''

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
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
                # G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                getCurrentOpinion(G)
                return
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

    # print(len(schedule))
    sorted_schedule = collections.OrderedDict(sorted(schedule.items()))
    # print(sorted_schedule)
    update_count = 0
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            adoption_list = list(G.neighbors(node))
            adoption_list.append(node)
            selected_node = np.random.choice([n for n in adoption_list])
            G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
            # G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.nodes[node] and G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (update, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == max_nodes:
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                getCurrentOpinion(G)
                return
            update_count+=1
            if update_count >= num_updates:
                getCurrentOpinion(G)
                return
    getCurrentOpinion(G)
    return

# voterModel(10, 5, 1000, 100)

# Below two functions are for simulation use
def voter(G, num_updates, process_time):
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
    # print(sorted_schedule)
    update_count = 1
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
                # G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == nx.number_of_nodes(G):
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                print("After %d iterations, consensus reached" % update_count)
                getCurrentOpinion(G)
                return update_count
            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                getCurrentOpinion(G)
                return update_count

    print("Process ends with %d iterations" % update_count)
    getCurrentOpinion(G)
    return update_count

def voterMajority(G, num_updates, process_time):
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
    # print(sorted_schedule)
    update_count = 1
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                neighbor_opi = G.nodes[node]['opinion']
                for neighbor in G.neighbors(node):
                    neighbor_opi += G.nodes[neighbor]['opinion']
                if neighbor_opi > 0:
                    G.nodes[node]['opinion'] = 1
                elif neighbor_opi == 0:
                    G.nodes[node]['opinion']= np.random.choice([-1, 1])
                else:
                    G.nodes[node]['opinion'] = -1
                # G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
            if getPosOpinion(G) == 0 or getPosOpinion(G) == nx.number_of_nodes(G):
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                print("After %d iterations, consensus reached" % update_count)
                getCurrentOpinion(G)
                return update_count
            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                getCurrentOpinion(G)
                return update_count

    print("Process ends with %d iterations" % update_count)
    getCurrentOpinion(G)
    return update_count



# used for simulation of N opinions
def addNFeature(G, no_opin ,num):
    stubborn_agents = random.sample(list(G), num)
    for node in G:
        G.nodes[node]['opinion'] = random.randint(1, no_opin)
        if node in stubborn_agents:
            G.nodes[node]['stubborness'] = 1
        else:
            G.nodes[node]['stubborness'] = 0
    return G

def reachConsensus(G):
    opin = nx.get_node_attributes(G, 'opinion')
    opinion = set()
    for k, v in opin.items():
        opinion.add(v)
    if len(opinion) == 1:
        return True
    return False

def getCurrentOpinionN(G):
    opin = nx.get_node_attributes(G, 'opinion')
    opinion = {}
    for k, v in opin.items():
        if v in opinion:
            opinion[v].append(k)
        else:
            opinion[v] = [k]
    print(opinion)
    return opinion



def setDistribution(G, no_opin):
    distribution = getCurrentOpinionN(G)
    for k, value in distribution.items():
        distribution[k] = len(value)
    for i in range(no_opin):
        if i+1 not in distribution:
            distribution[i+1]=0
    return distribution

def voterNOpinion(G, num_updates, process_time):
    addNFeature(G, 2, 0)
    getCurrentOpinionN(G)
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
    stable_count = 0
    stable = {}
    max_stable = G.number_of_nodes()
    update_count = 0
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
                # G.nodes[node]['opinion'] = G.nodes[np.random.choice([n for n in G.neighbors(node)])]['opinion']
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))
                current_opinion = getCurrentOpinionN(G)
            if reachConsensus(G):
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                print("After %d iterations, consensus reached" % update_count)
                getCurrentOpinionN(G)
                return update_count, 0

            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    print("After %d iterations, stable distributions reached" % update_count)
                    getCurrentOpinionN(G)
                    return update_count, 1
            else:
                stable = current_opinion.copy()
                stable_count = 0

            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                getCurrentOpinionN(G)
                return update_count, 2

    print("Process ends with %d iterations" % update_count)
    getCurrentOpinionN(G)
    return update_count, 2


def voterNOpiniontest(G, no_opin, num_updates, process_time):
    addNFeature(G, no_opin, 0)
    getCurrentOpinionN(G)
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
    update_count = 0
    stable_count = 0
    stable = {}
    max_stable = G.number_of_nodes() * 1.5
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
            current_opinion = getCurrentOpinionN(G)
            if reachConsensus(G):
                print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                return update_count, 0, distribution
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    return update_count, 1, distribution
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                return update_count, 2, distribution
    print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    return update_count, 2, distribution

# n, m, l = voterNOpinion(preferentialAttachment_2ndOrder(10, 0.5), 2, 10, 1200)
# print(n,m,l)




def voterNOpinionLPA(G, no_opin, num_updates, process_time):
    addNFeature(G, no_opin, 0)
    getCurrentOpinionN(G)
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
    # print(sorted_schedule)
    update_count = 0
    stable_count = 0
    stable = {}
    max_stable = 50
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                neighbor_opinion = [0] * no_opin
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)

                for neighbor in adoption_list:
                    # print("neighbor is %d"%neighbor)
                    opinion_neighbor = G.nodes[neighbor]['opinion']
                    # print("neighbor %d hold opinion %d "%(neighbor, opinion_neighbor))
                    neighbor_opinion[opinion_neighbor-1] += 1

                G.nodes[node]['opinion'] = neighbor_opinion.index(max(neighbor_opinion))+1
            current_opinion = getCurrentOpinionN(G)
            # print("At time %f, Node %d changed its opinion to %d. There are %d has pos opinion" %
            #       (time_t, node, G.nodes[node]['opinion'], getPosOpinion(G)))

            if reachConsensus(G):
                # print("At %f, after %d iterations, network reaches consensus" % (time_t, no_ite))
                print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                return update_count, 0, distribution

            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    return update_count, 1, distribution
            else:
                stable = current_opinion.copy()
                stable_count = 0

            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                return update_count, 2, distribution

    print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    return update_count, 2, distribution

# voterNOpinionLPA(nx.barabasi_albert_graph(10, 3), 3, 50, 10)
# n, m, l = voterNOpinionLPA(preferentialAttachment_2ndOrder(20, 0.5), 3, 500, 100)
# print(n, m, l)

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
    # print(sorted_events)
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



# voterMajority(nx.barabasi_albert_graph(50, 5), 10000, 100)

# voterModelStubborn(100, 50, 6000, 50, 10)

# voterModel(100, 50, 6000, 50)