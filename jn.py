import networkx as nx
import numpy as np
import pandas as pd
import math
import random
import collections
import matplotlib.pyplot as plt



# build graph
def completeGraph(no_node):
    return nx.complete_graph(no_node)

def starGraph(no_node):
    return nx.star_graph(no_node)

def smallWroldGraph(no_node, k):
    return nx.watts_strogatz_graph(no_node, k, 0.5)

def erdosRenyiGraph(no_node, p):
    return nx.fast_gnp_random_graph(no_node, p)

def randomSubset(repeated_nodes, no_edge):
    targets = set()
    while len(targets) < no_edge:
        x = random.choice(repeated_nodes)
        targets.add(x)
    return targets

def barabasiAlbertGraph(no_node, max_no_edge):
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
    return G

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
    return G



# Assign opinions to graphs
def addNFeature(G, no_opin ,num_of_stubborn):
    stubborn_agents = random.sample(list(G), num_of_stubborn)
    for node in G:
        G.nodes[node]['opinion'] = random.randint(1, no_opin)
        if node in stubborn_agents:
            G.nodes[node]['stubborness'] = 1
        else:
            G.nodes[node]['stubborness'] = 0
    return G



# Test if the graph reach consensus
def reachConsensus(G):
    opin = nx.get_node_attributes(G, 'opinion')
    opinion = set()
    for k, v in opin.items():
        opinion.add(v)
    if len(opinion) == 1:
        return True
    return False



# Get current opinion's distribution
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



# Voter model
def voterNOpinion(G, num_updates, process_time):
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
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
            if reachConsensus(G):
                print("After %d iterations, consensus reached" % update_count)
                getCurrentOpinionN(G)
                return update_count
            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                getCurrentOpinionN(G)
                return update_count
    print("Process ends with %d iterations" % update_count)
    getCurrentOpinionN(G)
    return update_count



# LPA
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
    update_count = 0
    stable_count = 0
    stable = {}
    max_stable = G.number_of_nodes()/5
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                neighbor_opinion = [0] * no_opin
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                for neighbor in adoption_list:
                    opinion_neighbor = G.nodes[neighbor]['opinion']
                    neighbor_opinion[opinion_neighbor-1] += 1
                G.nodes[node]['opinion'] = neighbor_opinion.index(max(neighbor_opinion))+1
                current_opinion = getCurrentOpinionN(G)
            if reachConsensus(G):
                print("After %d iterations, consensus reached" % update_count)
                getCurrentOpinionN(G)
                return update_count
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    print("After %d iterations, stable distributions reached" % update_count)
                    getCurrentOpinionN(G)
                    return update_count
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= num_updates:
                print("MAX updates reaches")
                getCurrentOpinionN(G)
                return update_count
    print("Process ends with %d iterations" % update_count)
    getCurrentOpinionN(G)
    return update_count



# for no_of_nodes = (100,250,500,750,1000), run the following:
def simulation(n, max_ite, max_time):
    # Create four dataframes

    # Run 100 times
    for i in range(100):
        # Create 6 graphs
        complete = completeGraph(n)
        star = starGraph(n - 1)
        sw = smallWroldGraph(n, n/10)
        er = erdosRenyiGraph(n, 0.5)
        pa = barabasiAlbertGraph(n, 5)
        pa2 = preferentialAttachment_2ndOrder(n, 0.5, False)
        graphs = [complete, star, sw, er, pa, pa2]

        # For these 6 graphs, apply voter models and LPA with binary opinions
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print(
                "--------------------------This is graph " + graph_name + " with 2 opinions--------------------------")
            graph_copy1 = graph.copy()
            addNFeature(graph_copy1, 2, 0)
            graph_copy2 = graph_copy1.copy()
            voter_ite_2 = voterNOpinion(graph_copy1, max_ite, max_time)
            LPA_ite_2 = voterNOpinionLPA(graph_copy2, 2, max_ite, max_time)
            # add to dataframe

        # For these 6 graphs, apply voter models and LPA with 3 opinions
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print(
                "--------------------------This is graph " + graph_name + " with 3 opinions--------------------------")
            graph_copy3 = graph.copy()
            addNFeature(graph_copy3, 3, 0)
            graph_copy4 = graph_copy3.copy()
            voter_ite_3 = voterNOpinion(graph_copy3, max_ite, max_time)
            LPA_ite_3 = voterNOpinionLPA(graph_copy4, 3, max_ite, max_time)
            # add to dataframe
