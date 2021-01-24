### Opinion Dynamics Model Simulation 

As the focus of the project is on discrete opinion models, we simulate two models - Voter model and its variation Label Propagation Algorithms. In this section, we firstly describe each model and corresponding algorithm used for implementation in Python. Then, we introduce our simulation - applying these two models to different graphs introduced above. In the last part, we analyze the simulation outcomes by comparing the convergence time between models and graphs. All simulations are implemented in Python code with library NetworkX. 

#### Details of Simulation Models 

##### Voter Model

Voter Model is proposed independently by Clifford and Sudbury, and by Holley and Liggett (Modeling Opinion Dynamics in Social Networks). According to Voter Model, in the graph, one node is randomly selected each time to update its opinion, adopting the opinion of one of its neighbor nodes (including itself) chosen uniformly at random. Intuitively, in a social network, at time $t$, one agent wakes up and randomly chooses one of its neighbors' opinion to adopt. 

To implement the Voter Model, we first need to generate a sequence of events to determine when each agent will wake up. Because Poisson process is used for modelling the times at which arrivals enter a system and the waking up time of a single agent can be considered as an arrival entering a system, we use Poisson process to generate the sequence of agent waking up events. According to the definition of Poisson process, the interarrival intervals $X_i$ follow an exponential distribution: $f_X(t)=\lambda e^{-\lambda t}$, for some real $\lambda > 0$, $t\geq 0$ (Discrete Stochastic Processes, Chapter 2: Poisson Processes). Note that parameter $\lambda$ is the rate of the process. For any time interval of size $t$, the expected number of arrivals in that interval is $\lambda t$. The above exponential distribution function is also the Probability Density Function (PDF) of $X_i$. From PDF, we can derive the Cumulative Distribution Function (CDF): $F_X(t)=\int ^t_0 \lambda e^{-\lambda x}dx = 1 - e^{-\lambda t}$. Using the Inverse-CDF technique, we find the inverse function of CDF is $F_X^{-1}(p)=-\frac{ln(1-p)}{\lambda} $. Now, with the inverse function of CDF, we can generate a sequence of interval times between wake-up of a single agent by setting $p\sim U(0,1)$. (https://towardsdatascience.com/the-poisson-process-everything-you-need-to-know-322aa0ab9e9a) 

Given a graph $G(V, E)$, the Voter Model we used in the simulation has input parameters: $n$ as the number of discrete opinions in network, $MAX\_TIME$ and $MAX\_RECORD$ limiting the number of updates that could happen in the graph. Due to the limiting time and computing power for simulation, we cannot let all models run until it reaches consensus. Therefore, we add $MAX\_TIME$ and $MAX\_RECORD$ to control. Besides, some networks may never have their agents' opinions converge. Accordingly, we add another terminate condition for step $4$ - terminate the process when there is a stable distribution of opinions in the network. More specifically, if the distribution of opinions remains the same after a certain number of iterations, we consider this network to have a stable distribution of agents' opinions and in some senses, reach consensus. The algorithm is implemented as following: 

1. Initialize the opinions of each node in the graph. For node $V_i$, its opinion $C_{V_i}(0)$ is randomly selected from $n$ discrete opinions at uniform. 
2. For each node $V_i$, set event time $T=0$ and repeat the following:
   - Generate $p$ following $U(0,1)$;
   - Calculate interval time $t$ by plugging $p$ the inverse function of CDF;
   - Update event time $T=T+t$ and record that node $V_i$ will wake up to change its opinion at time $T$; 
   - If $T\geq MAX\_TIME$,  terminate the repeating process.

3. Sort the record of nodes waking up in a chronological order. In each record, there are at least one nodes that will wake up. 
4. Follow the record order to wake up nodes and update its opinion. Repeat the following starting from the first record $a=1$: 
   - For each node $V_k$ in record $a$, update its opinion $c_k(a)$ by adopting the opinion of node $V_{l}$ selecting randomly at uniform from a set of nodes consisting of $V_k$ and $V_k$'s neighbor nodes $N_j=\left\{ j|\left(k,j\right)\in E\right\}$, i.e., $c_k(a)=c_l(a-1)$, where $V_l \in \left\{N_j\cap V_k\right\}$;
   - If all nodes reach consensus, i.e., $c_x(a)=c_y(a)$, for $\forall \;V_x, V_y \in \left\{V\right\}$, terminate the algorithm and return $a$; 
   - If graph $G$ has a stable distribution of nodes' opinions, i.e., the distribution of node's opinion does not changed after $q$ records, terminate the algorithm and return a. $q$ can be set equal to the number of nodes in graph $G$ times a coefficient $c$; 
   - Update $a=a+1$;
   - If $a>MAX\_RECORD$, terminate the algorithm, return $a$. 

With the returned $a$, we can learn how many updates it needs for the agents in the graph to reach consensus in Voter Model. 



##### Label Propagation Algorithm

Label Propagation Algorithm can be viewed as a variant of Voter Model. It is originally introduced by Albert, etc. to detect community structures in networks (Near linear time algorithm to detect community structures in large-scale networks) and the same updating method can be used in modelling opinion dynamics. Instead of adopting randomly selected neighbor's opinion, the node adopts the majority of neighbors' opinions. If there is a tie, this node choose one at random to adopt. Intuitively, in a social network, at time $t$, an agent wakes up and finds that most of its neighbors agree to opinion $i$, so it decided to change its own opinion to $i$. 

Given a graph $G(V, E)$, the Label Propagation Algorithm we used in the simulation has input parameters: $n$ as the number of discrete opinions in network, $MAX\_TIME$ and $MAX\_RECORD$ limiting the number of updates that could happen in the graph. The algorithm is implemented as follows: 

1. Initialize the opinions of each node in the graph. For node $V_i$, its opinion $C_{V_i}(0)$ is randomly selected from $n$ discrete opinions at uniform. 
2. For each node $V_i$, set event time $T=0$ and repeat the following:
   - Generate $p$ following $U(0,1)$;
   - Calculate interval time $t$ by plugging $p$ the inverse function of CDF;
   - Update event time $T=T+t$ and record that node $V_i$ will wake up to change its opinion at time $T$; 
   - If $T\geq MAX\_TIME$,  terminate the repeating process.

3. Sort the record of nodes waking up in a chronological order. In each record, there are at least one nodes that will wake up. 
4. Follow the record order to wake up nodes and update its opinion. Repeat the following starting from the first record $a=1$: 
   - For each node $V_k$ in record $a$, collect the opinion of $V_k$ and its neighbors $N_j=\left\{ j|\left(k,j\right)\in E\right\}$. Update $c_k(a)$ with the opinion with highest frequency. If there are multiple opinions with the same highest frequency, update $c_k(a)$ with one chosen randomly at uniform; 
   - If all nodes reach consensus, i.e., $c_x(a)=c_y(a)$, for $\forall \;V_x, V_y \in \left\{V\right\}$, terminate the algorithm and return $a$;
   - If graph $G$ has a stable distribution of nodes' opinions, i.e., the distribution of node's opinion does not changed after $q$ records, terminate the algorithm and return a. $q$ can be set equal to the number of nodes in graph $G$ times a coefficient $c$; 
   - Update $a=a+1$;
   - If $a>MAX\_RECORD$, terminate the algorithm, return $a$. 

With the returned $a$, we can learn how many updates it needs for the agents in the graph to reach consensus in Label Propagation Algorithm. 



#### Simulation on graphs

To simulate the above two models, we set the number of discrete opinions $n$ to be $2$ and $3$ in each model. This setting is based on real-life experience and help our simulation on real-life data next semester. When $n=2$, the system is a binary opinion model; in real life, U.S. president election (we only consider Biden and Trump here), conducting an investment or not can be considered as binary opinion model. When $n=3$, it can be applied in the case of trading stocks, to buy, to sell, or take no action. Correspondingly, we prepare $7$ graphs. They are $4$ deterministic graph topologies - complete graph, star graph, line graph, and cycle graph; and Erdos-Renyi graph, Barabasi-Albert graph, and two-level graph. To simulate social network, we set the number of nodes of each graph to be $(100, 250, 500, 750, 1000)$. 

Combined all above, we now have $2\;models\;*\;2 \;settings \;of\; opinions\; *\;7\;graphs\;*\;5\; settings\; of\; the\; number\; of\; nodes\;=\; 140$ scenarios in total, and each runs $100$ times. This could give us a general result in analyzing the convergence time because each experiment is i.i.d.. The overall methodology is illustrated as following: 

- FOR number of nodes $v  = (100,250,500,750,1000)$, repeat the following for $100$ times:
  - Create a complete graph $G_{complete}$, star graph $G_{star}$, line graph $G_{line}$, cycle graph $G_{cycle}$, Erdos-Renyi graph $G_{ER}$, Barabasi-Albert graph $G_{BA}$, and two-level graph $G_{2L}$. 
  - For each graph created, do the following: 
    - Run Voter Model with number of opinions $n=2$, and store the number of updates $a_{v2}$. 
    - Run Voter Model with number of opinions $n=3$, and store the number of updates $a_{v3}$. 
    - Run Label Propagation Algorithm with number of opinions $n=2$, and store the number of updates $a_{l2}$. 
    - Run Label Propagation Algorithm with number of opinions $n=3$, and store the number of updates $a_{l3}$. 



##### Comparison between different models



##### Comparison between different graphs







