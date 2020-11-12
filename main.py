from PA import *
from networkAnalysis import *
from plotGraph import *


def plotNetwork():
    # network = preferentialAttachmentV2(100)
    # preferentialAttachment(50, 100, loner=False)
    # network = preferentialAttachment_2ndOrder(100, 1)
    # network = preferentialAttachmentV1(100, 20)
    network = preferentialAttachment_MDApseudo(500, 50, 15)
    # network = preferentialAttachment_MDA(100, 50, 15)
    # degreeHistogram(nx.gnp_random_graph(100, 0.02))
    return network

def analysis(G):
    # fullAnalysis(network)
    interactiveGraphExtended(network)
    return


if __name__ == '__main__':
    network = plotNetwork()
    analysis(network)
