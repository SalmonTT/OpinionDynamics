import math
import collections
from PA import *

def initialize(G, num):
    stubborn_agents = random.sample(list(G), num)
    for node in G:
        G.nodes[node]['particle'] = 1
        if node in stubborn_agents:
            G.nodes[node]['stubborness'] = 1
        else:
            G.nodes[node]['stubborness'] = 0
    return G

def noParticle(G):
    particle = nx.get_node_attributes(G, 'particle')
    no_particle = 0
    for k, v in particle.items():
        if v == 1:
            no_particle += 1
    return no_particle

def randomWalk(G):
    no_stubborn = 0
    MAX_time = 10000
    initialize(G, no_stubborn)

    schedule = {}
    for node in G:
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= MAX_time:
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
            if G.nodes[node]['particle'] == 1 and G.nodes[node]['stubborness'] != 1:
                G.nodes[node]['particle'] = 0
                neighbor = np.random.choice([n for n in G.neighbors(node)])
                G.nodes[neighbor]['particle'] = 1
                # print("particle on node %d moves to node %d at time %f. Still %d particles left" %
                #       (node, neighbor, update, noParticle(G)))
            update_count += 1
            if noParticle(G) == 1 :
                print("Coalescing random walks ended with %d updates" % update_count )
                return

# For simulation use:
def rw(G, max_ite, MAX_time):
    schedule = {}
    for node in G:
        arrival_time = 0
        while True:
            p = np.random.uniform(0, 1)
            inter_arrival_time = - math.log(1.0 - p)
            arrival_time += inter_arrival_time
            if arrival_time <= MAX_time:
                if arrival_time in schedule:
                    schedule[arrival_time].append(node)
                else:
                    schedule[arrival_time] = [node]
            else:
                break

    sorted_schedule = collections.OrderedDict(sorted(schedule.items()))
    update_count = 1
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['particle'] == 1 and G.nodes[node]['stubborness'] != 1:
                G.nodes[node]['particle'] = 0
                neighbor = np.random.choice([n for n in G.neighbors(node)])
                G.nodes[neighbor]['particle'] = 1
                # print("particle on node %d moves to node %d at time %f. Still %d particles left" %
                #       (node, neighbor, update, noParticle(G)))
            update_count += 1
            if noParticle(G) == 1:
                print("Coalescing random walks ended with %d updates" % update_count)
                return update_count
            if update_count >= max_ite:
                print("MAX updates reaches")
                return update_count

# randomWalk(barabasiAlbertGraph(100,10))

# 3525
# 5311
# 9327
# 7854
# 5029
# 7219
# 7781
# 6842
# 3567
# 4235