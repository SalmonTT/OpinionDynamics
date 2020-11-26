from PA import *
from networkAnalysis import *
from plotGraph import *


def plotNetwork():
    # network = preferentialAttachmentV2(100)
    # preferentialAttachment(50, 100, loner=False)
    # network = preferentialAttachment_2ndOrder(100, 1)
    # network = preferentialAttachmentV3(500)
    # network = preferentialAttachment_MDApseudo(200, 50, 15)
    # network = preferentialAttachment_MDA(100, 50, 15)
    # degreeHistogram(nx.gnp_random_graph(100, 0.02))
    network = barabasiAlbertGraph(500, 10, seed=None)
    return network

def analysis(G):
    # fullAnalysis(network)
    interactiveGraphExtended(network)
    return


if __name__ == '__main__':
    network = plotNetwork()
    analysis(network)
