from buildGraph import *
from voter import *
from plotGraph import plotGraph
import pandas as pd
import matplotlib.pyplot as plt

def simulationMajority():
    # Set number of nodes and start building graph
    n = 100
    complete = completeGraph(n)
    star = starGraph(n-1)
    cycle = cycleGraph(n)
    line = lineGraph(n)
    # geometric = randomGeometricGraph(n, 0.1)
    er = erdosRenyiGraph(n, 0.5)
    pa = barabasiAlbertGraph(n, 10, seed=None)
    pa2 = preferentialAttachment_2ndOrder(n, 1, False)
    graphs = [complete, star, cycle, line, er, pa, pa2]

    # Voter algorithm starts
    max_ite = 10000
    max_time = 300
    print("Max iterations allowed is %d. Max process time is %d" % (max_ite, max_time))
    for graph in graphs:
        graph_name = [k for k, v in locals().items() if v == graph][0]
        print("--------------------------This is graph "+graph_name+"--------------------------" )
        addFeature(graph, 0)
        no_ite = voterMajority(graph, max_ite, max_time)
        # plotGraph(graph)
        print(no_ite)

def mulSimulationMajority():
    outcome = {'complete':[],
               'star':[],
               'cycle':[],
               'line':[],
               'er':[],
               'pa':[],
               'pa2':[]}

    for i in range(100):
        n = 100
        complete = completeGraph(n)
        star = starGraph(n - 1)
        cycle = cycleGraph(n)
        line = lineGraph(n)
        # geometric = randomGeometricGraph(n, 0.1)
        er = erdosRenyiGraph(n, 0.5)
        pa = barabasiAlbertGraph(n, 10, seed=None)
        pa2 = preferentialAttachment_2ndOrder(n, 1, False)
        graphs = [complete, star, cycle, line, er, pa, pa2]

        max_ite = 10000
        max_time = 300
        print("Max iterations allowed is %d. Max process time is %d" % (max_ite, max_time))
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print("--------------------------This is graph " + graph_name + "--------------------------")
            addFeature(graph, 0)
            ite = voterMajority(graph, max_ite, max_time)
            outcome[graph_name].append(ite)
            # plotGraph(graph)
            print()

    df = pd.DataFrame(outcome, columns = ['complete', 'star', 'cycle', 'line', 'er', 'pa', 'pa2'])
    print(df.head())
    df.to_csv(r'C:\Users\PP\Desktop\2020-21 Term1\SEEM FYP\Newrepo\OpinionDynamics\majority.csv',
              index=False, header=True)

def mulSimulationMajority1():
    outcome = {'complete':[],
               'star':[],
               'cycle':[],
               'line':[],
               'er':[],
               'pa':[],
               'pa2':[]}
    n = 100
    complete = completeGraph(n)
    star = starGraph(n - 1)
    cycle = cycleGraph(n)
    line = lineGraph(n)
    # geometric = randomGeometricGraph(n, 0.1)
    er = erdosRenyiGraph(n, 0.5)
    pa = barabasiAlbertGraph(n, 10, seed=None)
    pa2 = preferentialAttachment_2ndOrder(n, 1, False)
    graphs = [complete, star, cycle, line, er, pa, pa2]

    for i in range(100):
        max_ite = 10000
        max_time = 300
        print("Max iterations allowed is %d. Max process time is %d" % (max_ite, max_time))
        for graph in graphs:
            graph_name = [k for k, v in locals().items() if v == graph][0]
            print("--------------------------This is graph " + graph_name + "--------------------------")
            addFeature(graph, 0)
            ite = voterMajority(graph, max_ite, max_time)
            outcome[graph_name].append(ite)
            # plotGraph(graph)
            print()

    df = pd.DataFrame(outcome, columns = ['complete', 'star', 'cycle', 'line', 'er', 'pa', 'pa2'])
    print(df.head())
    df.to_csv(r'C:\Users\PP\Desktop\2020-21 Term1\SEEM FYP\Newrepo\OpinionDynamics\majority1.csv',
              index=False, header=True)

def csvAnalysis():
    df = pd.read_csv('majority1.csv')
    pd.set_option('display.expand_frame_repr', False)
    print(df.describe(include='all'))
    df.hist(figsize=(20, 20))
    plt.show()

# simulation()
# mulSimulationMajority()
# mulSimulationMajority1()
# csvAnalysis()