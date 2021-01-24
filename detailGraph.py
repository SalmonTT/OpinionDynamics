from majorSimulation import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import rcParams
import networkx as nx
from plotGraph import plotGraphWithNodeColorDependOnNodeDegree

'''
This file is used for Term 1 Final Report Detailed Simulation part, including
    -   Plot degree histogram, degree distribution, different graphs of networks
    -   Voter Model & LPA that could record the detail of opinion evolution (convergence time, type, distribution, ...)
    -   Different initial percentage of agents holding opinion 1
    -   Create a 7-node small community
'''

def degreeHistogram(G, no):
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
    if no == 1:
        plt.savefig('sw_degreeHistogram.jpg')
    elif no == 0:
        plt.savefig('ba_degreeHistogram.jpg')
    plt.show()

def degreeDistribution(G, no):
    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    plt.figure()
    plt.grid(True)
    plt.loglog(degrees[:], degree_freq[:], 'go-')
    plt.title('Social Network')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    if no == 1:
        plt.savefig('sw_degreeDistribution.jpg')
    elif no ==0:
        plt.savefig('ba_degreeDistribution.jpg')
    plt.show()

def detailplotGraphWithDegree(G, no):
    # polt netwrok with nodes' degree labeled
    degree_labels = {}
    for node in G.nodes():
        degree_labels[node] = G.degree(node)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False)
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='white')
    if no == 1:
        plt.savefig('sw_degree.jpg')
    elif no == 0:
        plt.savefig('ba_degree.jpg')
    plt.show()

def detailplotGraphWithNodeColorDependOnNodeDegree(G, no):
    # plot network with nodes' color depend on nodes' degree.
    # coolwarm: Red (Higher degree) --- Blue (Lower degree)
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            nodelist=D,
            node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=False,
            font_color='black')
    # for node in G.nodes():
    degree_labels = nx.get_node_attributes(G, "opinion")
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='black')
    if no == 1:
        plt.savefig('sw_degree_opinion.jpg')
    elif no ==0:
        plt.savefig('ba_degree_opinion.jpg')
    plt.show()

def detailplotGraphWithNodeColorDependOnNodeDegree1(G, no):
    # plot network with nodes' color depend on nodes' degree.
    # coolwarm: Red (Higher degree) --- Blue (Lower degree)
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            nodelist=D,
            node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=False,
            font_color='black')
    # for node in G.nodes():
    degree_labels = nx.get_node_attributes(G, "opinion")
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='black')
    if no == 1:
        plt.savefig('sw_degree_opinion_after_lpa.jpg')
    elif no==0:
        plt.savefig('ba_degree_opinion_after_lpa.jpg')
    plt.show()

def detailplotGraphWithNodeColorDependOnNodeDegreeVoter(G, no):
    # plot network with nodes' color depend on nodes' degree.
    # coolwarm: Red (Higher degree) --- Blue (Lower degree)
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            nodelist=D,
            node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=False,
            font_color='black')
    # for node in G.nodes():
    degree_labels = nx.get_node_attributes(G, "opinion")
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='black')
    if no == 1:
        plt.savefig('sw_degree_opinion_after_voter.jpg')
    elif no == 0:
        plt.savefig('ba_degree_opinion_after_voter.jpg')
    plt.show()

def updateOpin(G, opin):
    current_opin = nx.get_node_attributes(G, 'opinion')
    for k, v in current_opin.items():
        # print(k)
        opin[k].append(v)
    return opin

def detailvoterNOpinion(G, no_opin, max_iter, max_time, opin, no):
    start = process_time()
    opin = updateOpin(G, opin)
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
    max_stable = G.number_of_nodes() * 2
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                origin_opin = G.nodes[node]['opinion']
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                selected_node = np.random.choice([n for n in adoption_list])
                G.nodes[node]['opinion'] = G.nodes[selected_node]['opinion']
                # print("Node %d updates it opinion from %d to %d" % (node, origin_opin, G.nodes[node]['opinion']))
            opin = updateOpin(G, opin)
            current_opinion = getCurrentOpinionN(G)
            if reachConsensus(G):
                # print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                detailplotGraphWithNodeColorDependOnNodeDegreeVoter(G, no)
                return update_count, 0, distribution, opin
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    # print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    end = process_time()
                    print("time :", (end - start))
                    detailplotGraphWithNodeColorDependOnNodeDegreeVoter(G, no)
                    return update_count, 1, distribution, opin
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= max_iter:
                # print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                detailplotGraphWithNodeColorDependOnNodeDegreeVoter(G, no)
                return update_count, 2, distribution, opin
    # print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    end = process_time()
    print("time :", (end - start))
    detailplotGraphWithNodeColorDependOnNodeDegreeVoter(G, no)
    return update_count, 3, distribution, opin

# LPA
def detailvoterNOpinionLPA(G, no_opin, max_iter, max_time, opin, no):
    start = process_time()

    opin = updateOpin(G, opin)
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
    max_stable = G.number_of_nodes() * 2
    for update in sorted_schedule.keys():
        for node in sorted_schedule[update]:
            if G.nodes[node]['stubborness'] != 1:
                origin_opin = G.nodes[node]['opinion']
                neighbor_opinion = [0] * no_opin
                adoption_list = list(G.neighbors(node))
                adoption_list.append(node)
                for neighbor in adoption_list:
                    opinion_neighbor = G.nodes[neighbor]['opinion']
                    neighbor_opinion[opinion_neighbor - 1] += 1
                G.nodes[node]['opinion'] = neighbor_opinion.index(max(neighbor_opinion)) + 1
                # print("Node %d updates it opinion from %d to %d" %(node, origin_opin, G.nodes[node]['opinion']))
            opin = updateOpin(G, opin)
            current_opinion = getCurrentOpinionN(G)
            if reachConsensus(G):
                # print("After %d iterations, consensus reached" % update_count)
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                detailplotGraphWithNodeColorDependOnNodeDegree1(G, no)
                return update_count, 0, distribution, opin
            if stable == current_opinion:
                stable_count += 1
                if stable_count > max_stable:
                    # print("After %d iterations, stable distributions reached" % update_count)
                    distribution = setDistribution(G, no_opin)
                    end = process_time()
                    print("time :", (end - start))
                    detailplotGraphWithNodeColorDependOnNodeDegree1(G, no)
                    return update_count, 1, distribution, opin
            else:
                stable = current_opinion.copy()
                stable_count = 0
            update_count += 1
            if update_count >= max_iter:
                # print("MAX updates reaches")
                distribution = setDistribution(G, no_opin)
                end = process_time()
                print("time :", (end - start))
                detailplotGraphWithNodeColorDependOnNodeDegree1(G, no)
                return update_count, 2, distribution, opin
    # print("Process ends with %d iterations" % update_count)
    distribution = setDistribution(G, no_opin)
    end = process_time()
    print("time :", (end - start))
    detailplotGraphWithNodeColorDependOnNodeDegree1(G, no)
    return update_count, 3, distribution, opin

def detail():
    # create graphs
    sw = smallWroldGraph(30, 7)
    ba = barabasiAlbertGraph(30, 5)
    degreeHistogram(sw,1)
    degreeDistribution(sw,1)
    detailplotGraphWithDegree(sw,1)
    degreeHistogram(ba,0)
    degreeDistribution(ba,0)
    detailplotGraphWithDegree(ba,0)
    addNFeature(sw, 2, 0)
    addNFeature(ba, 2, 0)
    detailplotGraphWithNodeColorDependOnNodeDegree(sw, 1)
    detailplotGraphWithNodeColorDependOnNodeDegree(ba, 0)
    sw1 = sw.copy()
    ba1 = ba.copy()
    sw_node_list = sorted(sw.degree, key=lambda x: x[1], reverse=True)
    ba_node_list = sorted(ba.degree, key=lambda x: x[1], reverse=True)
    print(sw_node_list)
    print(ba_node_list)

    # create dict to store the change of opinions
    sw_opin = dict()
    ba_opin = dict()
    sw_opin_v = dict()
    ba_opin_v = dict()
    for i in range(30):
        sw_opin[i] = []
        ba_opin[i] = []
        sw_opin_v[i] = []
        ba_opin_v[i] = []
    sw_time, sw_type, sw_dis, sw_opin = detailvoterNOpinionLPA(sw, 2, 1000, 100, sw_opin,1)
    sw_time_v, sw_type_v, sw_dis_v, sw_opin_v = detailvoterNOpinion(sw1, 2, 1000, 100, sw_opin_v,1)
    print("For SW LPA, sw_time, sw_type, sw_dis are")
    print(sw_time, sw_type, sw_dis)
    print("For SW voter, sw_time, sw_type, sw_dis are")
    print(sw_time_v, sw_type_v, sw_dis_v)
    ba_time, ba_type, ba_dis, ba_opin = detailvoterNOpinionLPA(ba, 2, 1000, 100, ba_opin,0)
    ba_time_v, ba_type_v, ba_dis_v, ba_opin_v = detailvoterNOpinion(ba1, 2, 1000, 100, ba_opin_v,0)
    print("For BA LPA, ba_time, ba_type, ba_dis are")
    print(ba_time, ba_type, ba_dis)
    print("For BA voter, ba_time, ba_type, ba_dis are")
    print(ba_time_v, ba_type_v, ba_dis_v)


    sw_df = pd.DataFrame(sw_opin)
    ba_df = pd.DataFrame(ba_opin)
    sw_df_v = pd.DataFrame(sw_opin_v)
    ba_df_v = pd.DataFrame(ba_opin_v)
    sw_df.to_csv('sw_lpa.csv', index=False, header=True)
    ba_df.to_csv('ba_lpa.csv', index=False, header=True)
    sw_df_v.to_csv('sw_v.csv', index=False, header=True)
    ba_df_v.to_csv('ba_v.csv', index=False, header=True)

# detail()

# Assign opinions to graphs
def addCertainFeature(G, num_of_stubborn, percen):
    stubborn_agents = random.sample(list(G), num_of_stubborn)
    no_1 = int(G.number_of_nodes()*percen)
    print(no_1)
    random_nodes = set()
    while len(random_nodes)< no_1:
        i = random.randint(0, G.number_of_nodes()-1)
        random_nodes.add(i)

    for node in G:
        G.nodes[node]['opinion'] =2
        if node in stubborn_agents:
            G.nodes[node]['stubborness'] = 1
        else:
            G.nodes[node]['stubborness'] = 0

    for node in random_nodes:
        G.nodes[node]['opinion']=1

    return G


def assignDifferentOpinions():
    # ba3 = smallWroldGraph(50, 8)
    ba3 = barabasiAlbertGraph(30, 5)
    degreeHistogram(ba3, 3)
    detailplotGraphWithDegree(ba3, 3)
    ba2 = ba3.copy()
    ba4 = ba3.copy()
    ba5 = ba3.copy()
    addCertainFeature(ba2, 0, 0.2)
    # detailplotGraphWithNodeColorDependOnNodeDegree(ba2, 3)
    getCurrentOpinionN(ba2, True)
    addCertainFeature(ba3, 0, 0.3)
    # detailplotGraphWithNodeColorDependOnNodeDegree(ba3, 3)
    getCurrentOpinionN(ba3, True)
    addCertainFeature(ba4, 0, 0.4)
    # detailplotGraphWithNodeColorDependOnNodeDegree(ba4, 3)
    getCurrentOpinionN(ba4, True)
    addCertainFeature(ba5, 0, 0.5)
    # detailplotGraphWithNodeColorDependOnNodeDegree(ba5, 3)
    getCurrentOpinionN(ba5, True)
    graphs = [ba2, ba3, ba4, ba5]

    # for graph in graphs:
    for i in range(4):
        graph = graphs[i]
        print("this is for graph ba%d--------------------------------------------------" %i )
        for j in range(1):
            print("iteration %d "%j)
            gv = graph.copy()
            glpa = graph.copy()
            opin_lpa = dict()
            opin_v = dict()
            for k in range(30):
                opin_v[k] = []
                opin_lpa[k] = []
            time, type, dis, opin_lpa = detailvoterNOpinionLPA(gv, 2, 10000, 500, opin_lpa, 3)
            time_v, type_v, dis_v, opin_v = detailvoterNOpinion(glpa, 2, 10000, 500, opin_v, 3)
            print("For LPA, sw_time, sw_type, sw_dis are" )
            print(time, type, dis)
            print("For voter, sw_time, sw_type, sw_dis are" )
            print(time_v, type_v, dis_v)

            df_v = pd.DataFrame(opin_v)
            df_lpa = pd.DataFrame(opin_lpa)
            filename_v = "%s_v_%s.csv" %("ba"+str(i+3), str(j))
            filename_lpa = "%s_lpa_%s.csv" % ("ba"+str(i+3), str(j))
            df_v.to_csv(filename_v, index=False, header=True)
            df_lpa.to_csv(filename_lpa, index=False, header=True)


# assignDifferentOpinions()

def plotDegree(G):
    # plot network with nodes' color depend on nodes' degree.
    # coolwarm: Red (Higher degree) --- Blue (Lower degree)
    D = dict(G.degree)
    low, *_, high = sorted(D.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
    rcParams['figure.figsize'] = 12, 7
    pos = nx.fruchterman_reingold_layout(G)
    nx.draw(G, pos,
            nodelist=D,
            node_size=1000,
            node_color=[mapper.to_rgba(i)
                        for i in D.values()],
            with_labels=False,
            font_color='white')
    # for node in G.nodes():
    degree_labels = nx.get_node_attributes(G, "opinion")
    nx.draw_networkx_labels(G, pos, labels=degree_labels, font_size=10, font_color='black')
    plt.show()


def smallCommunity():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    G.add_edge(0, 3)
    G.add_edge(0, 5)
    G.add_edge(0, 6)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.nodes[0]['opinion'] = 2
    G.nodes[1]['opinion'] = 1
    G.nodes[3]['opinion'] = 2
    G.nodes[5]['opinion'] = 1
    G.nodes[2]['opinion'] = 3
    G.nodes[4]['opinion'] = 3
    G.nodes[6]['opinion'] = 2
    for i in range(6):
        G.nodes[i]['stubborness'] = 0
    plotGraphWithNodeColorDependOnNodeDegree(G)
    # plotDegree(G)
    # gv = G.copy()
    # glpa = G.copy()
    # opin_lpa = dict()
    # opin_v = dict()
    # for k in range(7):
    #     opin_v[k] = []
    #     opin_lpa[k] = []
    # time, type, dis, opin_lpa = detailvoterNOpinionLPA(gv, 3, 10000, 500, opin_lpa, 3)
    # time_v, type_v, dis_v, opin_v = detailvoterNOpinion(glpa, 3, 10000, 500, opin_v, 3)
    # print("For LPA, sw_time, sw_type, sw_dis are")
    # print(time, type, dis)
    # print("For voter, sw_time, sw_type, sw_dis are")
    # print(time_v, type_v, dis_v)
    #
    # df_v = pd.DataFrame(opin_v)
    # df_lpa = pd.DataFrame(opin_lpa)
    # df_v.to_csv("voter.csv", index=False, header=True)
    # df_lpa.to_csv("lpa.csv", index=False, header=True)
