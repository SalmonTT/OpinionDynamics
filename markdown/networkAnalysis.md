# Network Analysis

Prior to simulation of opinion dynamics models, we must first create a complex network in order to resemble the topology of real networks. Since the 1950's, random graphs, described as "large scale networks with no apparent design principles" (Albert & Barabasi, 2001) has been the most straightforward realization of a complex network. The earliest study of random graphs were conducted by Paul Erdos and Alfred Renyi (). According to the Erdos-Renyi (ER) model, a graph starts with N nodes, and connect every pair of nodes with probability *p*. This creates a graph with approximately $pN(N-1)/2$ edges distributed randomly. 

In recent years, three key concepts have been defined to create complex networks which simulates real networks more closely. 

1) *Small worlds*
> This concept states that there exists a relatively short path between any two nodes in networks, including those of large sizes. In terms of sociology, this is manifested by the famous "six degrees of separation" concept proposed by social psychologist Stanley Milgram (1967). Specifically, it states that there exists a path of acquaintances with average length of six between most pairs of people in the United States (Kochen 1989)

2) *Clustering*
> Cliques, which are circles of friends or acquaintances in which every member knows every other member, often forms in social networks. This property is quantified by the clustering coefficient (Watts and Strogatz 1998). Given a selected node *i* which has $k_i$ neighbors, if the first neighbors of node *i* form part of a clique, there would be $k_i(k_i-1)/2$ edges between them. The ratio between the number of edges $E_i$ that actually exists between them and $k_i(k_i-1)/2$ gives the value of the clustering coefficient:
$$
C_i=\frac{2E_i}{k_i(k_i-1)}
$$
Watts and Strogatz pointed out that the clustering coefficient of real networks is typically much larger than most, if not all, random networks of equal number of nodes and edges. 

3) *Degree distribution*

> Degree distribution of a network is often characterized by the the distribution function $P(k)$, which gives the probability that a randomly selected node has exactly *k* edges. Empirical studies have shown that a large number of real networks, such as the World-Wide Web (Albert, Jeong, Barabasi 1999), Internet (Faloutso *et al.* 1999) and metabolic networks (Jeong *et al.* 2000), follows a power-law tail degree distribution:
$$
P(k) \sim k^{-\gamma}
$$
> Networks that follow this degree distribution are generally called scale-free networks. 

In the following section, we will take a look at three main classes of complex network models: random graphs, small world models, and scale-free models. While random graphs may seem like a poor representation of real networks, they are still widely used as benchmark for many studies. Small world models are included as they incorporate of the clustering (or formation of cliques) characteristics of real networks. And finally, scale-free models are used as they are constructed with the consideration that power-law degree distribution are often found in real networks. In addition, we will also take a look at regular graphs as well as other types of graph structures. The complete list is as follows:

(Deterministic topology)

> <u>Random Graphs</u>: Erdos-Renyi Model
> <u>Small World Model</u>: Small world?
> <u>Scale-free Model</u>: Preferential Attachment Model (A.K.A. Barabasi-Albert Model)
> <u>Regular Graphs</u>: Complete Graph, Cycle Graph
> <u>Other Graphs</u>: Line Graph, Star Graph

For each class of complex network:

- Concept
- code if applicable 
- properties:
  - degree distribution 
  - 10 nodes: density, betweenness, graph (visual)
  - scalability: 20nodes, 50 nodes...