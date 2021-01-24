import networkx as nx
import numpy as np
import pandas as pd
import math
import random
import collections
import matplotlib.pyplot as plt
from time import process_time

'''
This file is for Term 1 Final Report Major Simulation of Voter Model and LPA, including
    -   Create graphs of different topologies
    -   Repeat 100 times on the same graph for Voter Model and LPA
'''

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
def addNFeature(G, no_opin, num_of_stubborn):
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
def getCurrentOpinionN(G, print_opinion=False):
    opin = nx.get_node_attributes(G, 'opinion')
    opinion = {}
    for k, v in opin.items():
        if v in opinion:
            opinion[v].append(k)
        else:
            opinion[v] = [k]
    if print_opinion:
        print(opinion)
    return opinion



# set the returned distribution
def setDistribution(G, no_opin):
    distribution = getCurrentOpinionN(G)
    for k, value in distribution.items():
        distribution[k] = len(value)
    for i in range(no_opin):
        if i + 1 not in distribution:
            distribution[i + 1] = 0
    return distribution



# Voter model
def voterNOpinion(G, no_opin, max_iter, max_time):
    start = process_time()
    getCurrentOpinionN(G)
    schedule = {}
    for node in G:
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= max_time:
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
    max_stable = G.number_of_nodes() * 0.7
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
            current_opinion = getCurrentOpinionN(G, False)
            if reachConsensus(G):
                # print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                return update_count, 0, distribution
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    # print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    end = process_time()
                    print("time :", (end - start))
                    return update_count, 1, distribution
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= max_iter:
                # print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                return update_count, 2, distribution
    # print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    end = process_time()
    print("time :", (end - start))
    return update_count, 3, distribution



# LPA
def voterNOpinionLPA(G, no_opin, max_iter, max_time):
    start = process_time()
    addNFeature(G, no_opin, 0)
    getCurrentOpinionN(G)
    schedule = {}
    for node in G:
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= max_time:
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
    max_stable = G.number_of_nodes() * 1.2
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                neighbor_opinion = [0] * no_opin
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                for neighbor in adoption_list:
                    opinion_neighbor = G.nodes[neighbor]['opinion']
                    neighbor_opinion[opinion_neighbor - 1] += 1
                G.nodes[node]['opinion'] = neighbor_opinion.index(max(neighbor_opinion)) + 1
            current_opinion = getCurrentOpinionN(G, False)
            if reachConsensus(G):
                # print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                return update_count, 0, distribution
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    # print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    end = process_time()
                    print("time :", (end - start))
                    return update_count, 1, distribution
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= max_iter:
                # print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                return update_count, 2, distribution
    # print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    end = process_time()
    print("time :", (end - start))
    return update_count, 3, distribution



# for no_of_nodes = (100,250,500,750,1000), run the following:
def simulation(n, max_iter, max_time):
    simulation_start = process_time()
    # Create four dataframes, timeType = 1 means it reaches stable distribution, 0 means it reaches consensus,
    # 2 means meet MAX iterations
    voter_2 = {
        # 'Complete_time': [], 'Complete_timeType': [], 'Complete_opinion1': [],
        #        'Star_time': [], 'Star_timeType': [], 'Star_opinion1': [],
               'SW_time': [], 'SW_timeType': [], 'SW_opinion1': [],
               'ER_time': [], 'ER_timeType': [], 'ER_opinion1': [],
               'PA_time': [], 'PA_timeType': [], 'PA_opinion1': [],
               'L2_time': [], 'L2_timeType': [], 'L2_opinion1': []}
    voter_3 = {
        # 'Complete_time': [], 'Complete_timeType': [], 'Complete_opinion1': [], 'Complete_opinion2': [],
        #        'Star_time': [], 'Star_timeType': [], 'Star_opinion1': [], 'Star_opinion2': [],
               'SW_time': [], 'SW_timeType': [], 'SW_opinion1': [], 'SW_opinion2': [],
               'ER_time': [], 'ER_timeType': [], 'ER_opinion1': [], 'ER_opinion2': [],
               'PA_time': [], 'PA_timeType': [], 'PA_opinion1': [], 'PA_opinion2': [],
               'L2_time': [], 'L2_timeType': [], 'L2_opinion1': [], 'L2_opinion2': []}
    LPA_2 = {
        # 'Complete_time': [], 'Complete_timeType': [], 'Complete_opinion1': [],
        #        'Star_time': [], 'Star_timeType': [], 'Star_opinion1': [],
               'SW_time': [], 'SW_timeType': [], 'SW_opinion1': [],
               'ER_time': [], 'ER_timeType': [], 'ER_opinion1': [],
               'PA_time': [], 'PA_timeType': [], 'PA_opinion1': [],
               'L2_time': [], 'L2_timeType': [], 'L2_opinion1': []}
    LPA_3 = {
        # 'Complete_time': [], 'Complete_timeType': [], 'Complete_opinion1': [], 'Complete_opinion2': [],
        #        'Star_time': [], 'Star_timeType': [], 'Star_opinion1': [], 'Star_opinion2': [],
               'SW_time': [], 'SW_timeType': [], 'SW_opinion1': [], 'SW_opinion2': [],
               'ER_time': [], 'ER_timeType': [], 'ER_opinion1': [], 'ER_opinion2': [],
               'PA_time': [], 'PA_timeType': [], 'PA_opinion1': [], 'PA_opinion2': [],
               'L2_time': [], 'L2_timeType': [], 'L2_opinion1': [], 'L2_opinion2': []}

    # Run 100 times
    for i in range(25):
        print("iteration: %d" % i)
        # Create 6 graphs
        # Complete = completeGraph(n)
        # Star = starGraph(n - 1)
        # Update it according to n
        SW = smallWroldGraph(n,40)
        ER = erdosRenyiGraph(n, 0.06)
        # Update it according to n
        PA = barabasiAlbertGraph(n, 25)
        L2 = preferentialAttachment_2ndOrder(n, 1, False)
        # graphs = [Complete, Star, SW, ER, PA, L2]
        graphs = [SW, ER, PA, L2]

        # For these 6 graphs, apply voter models and LPA with binary opinions
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print('iteration %d, binary voter, graph %s' % (i, graph_name))
            # print(
            #     "--------------------------This is graph " + graph_name + " with 2 opinions--------------------------")
            graph_copy1 = graph.copy()
            addNFeature(graph_copy1, 2, 0)
            graph_copy2 = graph_copy1.copy()
            # print("This is for voter model------------------------------")
            voter_ite_2, voter_2_stable, voter_2_distribution = voterNOpinion(graph_copy1, 2, max_iter, max_time)
            # print("This is for LPA------------------------------")
            LPA_ite_2, LPA_2_stable, LPA_2_distribution = voterNOpinionLPA(graph_copy2, 2, max_iter, max_time)
            # add to dataframe
            voter_2[graph_name + '_time'].append(voter_ite_2)
            voter_2[graph_name + '_timeType'].append(voter_2_stable)
            voter_2[graph_name + '_opinion1'].append(voter_2_distribution.get(1))
            LPA_2[graph_name + '_time'].append(LPA_ite_2)
            LPA_2[graph_name + '_timeType'].append(LPA_2_stable)
            LPA_2[graph_name + '_opinion1'].append(LPA_2_distribution.get(1))

        # For these 6 graphs, apply voter models and LPA with 3 opinions
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print('iteration %d, 3-opinion voter, graph %s' % (i, graph_name))
            # print(
            #     "--------------------------This is graph " + graph_name + " with 3 opinions--------------------------")
            graph_copy3 = graph.copy()
            addNFeature(graph_copy3, 3, 0)
            graph_copy4 = graph_copy3.copy()
            # print("This is for voter model------------------------------")
            voter_ite_3, voter_3_stable, voter_3_distribution = voterNOpinion(graph_copy3, 3, max_iter, max_time)
            # print("This is for LPA------------------------------")
            LPA_ite_3, LPA_3_stable, LPA_3_distribution = voterNOpinionLPA(graph_copy4, 3, max_iter, max_time)
            # add to dataframe
            voter_3[graph_name + '_time'].append(voter_ite_3)
            voter_3[graph_name + '_timeType'].append(voter_3_stable)
            voter_3[graph_name + '_opinion1'].append(voter_3_distribution.get(1))
            voter_3[graph_name + '_opinion2'].append(voter_3_distribution.get(2))
            LPA_3[graph_name + '_time'].append(LPA_ite_3)
            LPA_3[graph_name + '_timeType'].append(LPA_3_stable)
            LPA_3[graph_name + '_opinion1'].append(LPA_3_distribution.get(1))
            LPA_3[graph_name + '_opinion2'].append(LPA_3_distribution.get(2))

    voter_2_df = pd.DataFrame(voter_2, columns=[
        # 'Complete_time', 'Complete_timeType', 'Complete_opinion1',
        #                                         'Star_time', 'Star_timeType', 'Star_opinion1',
                                                'SW_time', 'SW_timeType', 'SW_opinion1',
                                                'ER_time', 'ER_timeType', 'ER_opinion1',
                                                'PA_time', 'PA_timeType', 'PA_opinion1',
                                                'L2_time', 'L2_timeType', 'L2_opinion1'])
    LPA_2_df = pd.DataFrame(LPA_2, columns=[

        # 'Complete_time', 'Complete_timeType', 'Complete_opinion1',
        #                                         'Star_time', 'Star_timeType', 'Star_opinion1',
                                                'SW_time', 'SW_timeType', 'SW_opinion1',
                                                'ER_time', 'ER_timeType', 'ER_opinion1',
                                                'PA_time', 'PA_timeType', 'PA_opinion1',
                                                'L2_time', 'L2_timeType', 'L2_opinion1'])
    voter_3_df = pd.DataFrame(voter_3, columns=[
        # 'Complete_time', 'Complete_timeType', 'Complete_opinion1', 'Complete_opinion2',
        #                                         'Star_time', 'Star_timeType', 'Star_opinion1', 'Star_opinion2',
#                                         'SW_time', 'SW_timeType', 'SW_opinion1', 'SW_opinion2',

                                                'SW_time', 'SW_timeType', 'SW_opinion1', 'SW_opinion2',
                                                'ER_time', 'ER_timeType', 'ER_opinion1', 'ER_opinion2',
                                                'PA_time', 'PA_timeType', 'PA_opinion1', 'PA_opinion2',
                                                'L2_time', 'L2_timeType', 'L2_opinion1', 'L2_opinion2'])
    LPA_3_df = pd.DataFrame(LPA_3, columns=[
        # 'Complete_time', 'Complete_timeType', 'Complete_opinion1', 'Complete_opinion2',
        #                                         'Star_time', 'Star_timeType', 'Star_opinion1', 'Star_opinion2',
                                                'SW_time', 'SW_timeType', 'SW_opinion1', 'SW_opinion2',
                                                'ER_time', 'ER_timeType', 'ER_opinion1', 'ER_opinion2',
                                                'PA_time', 'PA_timeType', 'PA_opinion1', 'PA_opinion2',
                                                'L2_time', 'L2_timeType', 'L2_opinion1', 'L2_opinion2'])
    print(voter_2_df.head())
    print(LPA_2_df.head())
    print(voter_3_df.head())
    print(LPA_3_df.head())
    voter_2_df.to_csv('voter2_node500.csv', index=False, header=True)
    LPA_2_df.to_csv('LPA2_node500.csv', index=False, header=True)
    voter_3_df.to_csv('voter3_node500.csv', index=False, header=True)
    LPA_3_df.to_csv('LPA3_node500.csv', index=False, header=True)
    simulation_end = process_time()
    print("simulation time: ", simulation_end-simulation_start)

def testTime(n, max_iter, max_time):
    Complete = completeGraph(n)
    Star = starGraph(n - 1)
    # Update it according to n
    SW = smallWroldGraph(n, int(n / 10))
    ER = erdosRenyiGraph(n, 0.5)
    # Update it according to n
    PA = barabasiAlbertGraph(n, 10)
    L2 = preferentialAttachment_2ndOrder(n, 0.5, False)
    graphs = [Complete, Star, SW, ER, PA, L2]
    for graph in graphs:
        graph_name = [k for k, v in locals().items() if v == graph][0]
        graph_copy1 = graph.copy()
        addNFeature(graph_copy1, 2, 0)
        graph_copy2 = graph_copy1.copy()
        voter_ite_2, voter_2_stable, voter_2_distribution = voterNOpinion(graph_copy1, 2, max_iter, max_time)
        LPA_ite_2, LPA_2_stable, LPA_2_distribution = voterNOpinionLPA(graph_copy2, 2, max_iter, max_time)
        print("%s binary opinion voter: iteration = %d - %d, type = %d - %d" % (graph_name, voter_ite_2, LPA_ite_2, voter_2_stable, LPA_2_stable))

        graph_copy3 = graph.copy()
        addNFeature(graph_copy3, 3, 0)
        graph_copy4 = graph_copy3.copy()
        voter_ite_3, voter_3_stable, voter_3_distribution = voterNOpinion(graph_copy3, 3, max_iter, max_time)
        LPA_ite_3, LPA_3_stable, LPA_3_distribution = voterNOpinionLPA(graph_copy4, 3, max_iter, max_time)
        print("%s 3 opinion voter: iteration = %d - %d, type = %d - %d" % (
        graph_name, voter_ite_3, LPA_ite_3, voter_3_stable, LPA_3_stable))


# simulation(750, 10000, 500)