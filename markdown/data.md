Everytime (out of 100 times) do the following for each opinion dynamics model-network combination:

- Store the <u>convergence time</u> (in terms of iterations)
  - In case of taking too long to converge (longer than max. iteration [1] ), apply early stopping condition [2] . Store the number of iterations before early stopping is applied (<u>appx. convergence time</u>)
- Store the distribution of opinions at 0% of max. iteration, 25% of iteration, 50% of iteration, 75% of iteration [3]
  - Why? we want to see if there is a sudden point in time (iteration) where the the distribution of opinions undergo significant change (e.g. from even distribution 5-5 to uneven distribution 7-3)
- Opinion evolution of the KOL (max degree node) and opinion evolution of average node (degree = average (or median) degree of network)
  - Perhaps opinion at 0%, 25%, 50%, 75% of iteration
  - Why? See if the evolution of the opinion is different between the two, and compare with distribution of opinion at the time
- Store the general properties of the network [4]
  - Max degree
  - Min degree
  - num. of clusters
  - etc. 
    - Why? We want to see if convergence time is correlated with network properties
- 