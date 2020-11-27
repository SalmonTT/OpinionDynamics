Reason for choosing parameters for different graphs

Both Barabasi-Albert algorithm and two-level algorithm are used produce scale-free network. For Barabasi-Albert algorithm, we have a parameter $MAX\_EDGE$ to limit the max number of edges a newly-added node can build with existing nodes. For two-level algorithm, we have a coefficient $p$ to how important the opinions of node $V_{i}$'s second-order neighbors (neighbors' neighbors) is in determining the probability of the newly-added node connect to $V_i$. We set $MAX\_EDGE=(10,15,20,25,30)$, $p = (0.5,0.5,0.8,1,1)$ for number of nodes $n=(100,250,500,750,1000)$ respectively. With these setting, we can observe a general degree distribution as in figure(), indicating that the nodes with high degrees are rare and most of nodes have low degrees in these two graphs. We can find similar scenarios in real world: in social network, KOLs usually have large amount of followers and the number of KOLs is small,while normal users have much less followers and the number of normal users are large.  

We use small-world graph to resemble the real-world by setting its number of nodes $k$ in the initial cluster to be $(10,20,30,40,50)$ for number of nodes $n=(100,250,500,750,1000)$ respectively. We imitate the real world groups by limiting $k$. For Erdos-Renyi graph, we can consider is as a random generated graph and we set the probability of edge creation $p = (0.1,0.1,0.08,0.06,0.05)$ number of nodes $n=(100,250,500,750,1000)$ respectively. This setting provide Erdos-Renyi graphs with nodes degree centrals at around $15$ for $n=100$ to around $50$ for $n=1000$, imitating real world situations. 





Network Analysis

- Target graphs: ER, SW, PA, 2L
- Number of Nodes: 25
- Model: Voter, LPA
- Opinions: 2, 3

To better understand how each agent updates their opinions in detail, we now look at the process of Voter Model and Label Propagation Algorithm. For the purpose of imitate real world scenarios, we investigate Erdos-Renyi graph, small-world graph, Barabasi-Albert graph, and two-level graph with the number of nodes equal to $25$. 

1. Generate ER, SW, PA, 2L graph with number of nodes $n=25$. For each graph $G$, run the following: 
   - Create 2 copies of $G$ as $G_{2,voter}$ and $G_{3,voter}$. 
   - Assign binary opinions to nodes in $G_{2,voter}$ uniformly at random. Create a copy of  $G_{2,voter}$ as $G_{2,LPA}$. 
   - Assign 3 opinions to nodes in $G_{3,voter}$ uniformly at random. Create a copy of  $G_{3,voter}$ as $G_{3,LPA}$.
   - For $G_{2,voter}$ run Voter model and record every node's opinion at every updates. 
   - For $G_{3,voter}$ run Voter model and record every node's opinion at every updates. 
   - For $G_{2,LPA}$ run LPA and record every node's opinion at every updates. 
   - For $G_{3,LPA}$ run LPA and record every node's opinion at every updates. 

2. Analyze the process and have the following data:
   - The distribution of opinions at 0% of max. update, 25% of update, 50% of update, 75% of update, 100% of update
   - The opinion evolution of max degree node
   - The opinion evolution of nodes with degree equal to the mode of nodes' degrees
   - The opinion evolution of min degree node



Analyze simulation result

We analyze the simulation result by comparing from different models. 

We firstly check the convergence type of each iterations. We have $4$ convergence types - terminate because of reaching consensus, terminate because of reaching stable distribution, terminate because of reaching $MAX\_ITE$, terminate because of reaching $MAX\_TIME$. We consider the first two results as converge successfully, the last two as converge failed. 

We consider for each models (voter 2&3, LPA 2&3):

- how many is a success convergence
- as the number of nodes increase, the proportion of convergence types change?
- for different graphs, the proportion of convergence types vary?

Then we take a close look at the those converging successfully. We can consider:

- the convergence time's mean, std, min, 25%, 50%, 75%, max, top10, last10
- find possible relations of the convergence time and models, graphs, number of nodes

For those who reaches stable distribution, we take a look at its opinion distribution and may conclude:?

For those who fails in converge, we take a look at its opinion distribution and may conclude:?


Go through the results of each 












