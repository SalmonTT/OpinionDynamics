from PA import *
from networkAnalysis import *
from plotGraph import *


def plotNetwork():
    network = preferentialAttachmentV1(50, 100)
    # preferentialAttachment(50, 100, loner=False, max_p=0.7)
    # preferentialAttachment_2ndOrder(100, 6, max_p=0.8)
    # preferentialAttachment_MDA(20, 100, 14)
    # degreeHistogram(nx.gnp_random_graph(100, 0.02))
    return network

def analysis(G):
    fullAnalysis(network)
    interactiveGraphExtended(network)
    return

if __name__ == '__main__':
    network = plotNetwork()
    analysis(network)