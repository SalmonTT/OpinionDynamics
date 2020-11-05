# https://towardsdatascience.com/the-poisson-process-everything-you-need-to-know-322aa0ab9e9a
# voting models in random networks
from PA import *
from pyvis.network import Network
from scipy.stats import poisson

def interactiveGraphWithOpinion(G):
    # plot interactive graph using pyvis, with degree, no of node labeled, size depends on nodes' degree
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    nt.barnes_hut(spring_strength=0.006)
    for node in G:
        nt.add_node(node, label=G.degree(node), title="node "+str(node)+' '+str(G.nodes[node]['opinion']), value=G.degree(node))

    for edge in G.edges:
        nt.add_edge(int(edge[0]), int(edge[1]), color='white')
    nt.show("nx.html")

def voterV1(max_nodes, num_updates):
    # step one: create a social network
    graph = preferentialAttachmentV1(max_nodes)
    # step three: iterate through n number of updates
    for k in range(num_updates):
        # for each update k, update j number of nodes opinions via Poisson process with lamba=1 following voter algorithm
        # get a list of nodes that needs to be updated:
        print(str(k) + " round" + " node 5 opinion: "+str(graph.nodes[5]['opinion']))
        p = poisson.pmf(1, 1)
        update_nodes = []
        all_nodes = list(range(max_nodes))
        for node in all_nodes:
            if np.random.uniform(0, 1) < p:
                update_nodes.append(node)
        for node in update_nodes:
            graph.nodes[node]['opinion'] = graph.nodes[random.choice([n for n in graph.neighbors(node)])]['opinion']

    interactiveGraphWithOpinion(graph)
    return


voterV1(100, 50)

