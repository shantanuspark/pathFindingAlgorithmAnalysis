# pathFindingAlgorithmAnalysis
Analyzed performance of A*, Genetic and Greedy algorithms on travelling salesman problem on the DIMACS dataset

Traveling Salesman problem, defined in the 1800s by the Mathematicians W.R.Hamilton and Thomas Kirkman, is a classic algorithmic problem
in the field of Computer Science[1]. In this experiment, traveling salesman problem is solved using A*, Genetic and Greedy algorithms.
DIMACS dataset is used to benchmark the performance of the three algorithms. It is clear from the observations that greedy algorithm is very
fast but comparatively less optimal, where as genetic algorithm depends a lot on the initial parameters like mutation rate, no. of generations,
crossover rate and population size, tweaking these parameters impact the speed and the best tour length generated. A* algorithm does produces
optimal results but is more time consuming.

The three files, hw4_astar.py, hw4_greedy.py and pyevolve_ex12_tsp.py are the python scripts of astar, greedy and genetic TSP algorithms.

The A* TSP implementation here is adapted from Dr. Huan Liu as stated <a href="http://www.public.asu.edu/~huanliu/AI04S/project1.htm">here</a>
Initial State: Agent in the start city and has not visited any other city
Goal State: Agent has visited all the cities and reached the start city again
Successor Function: Generates all cities that have not yet visited
Edge-cost: distance between the cities represented by the nodes, use this cost to calculate g(n).
h(n): distance to the nearest unvisited city from the current city + estimated distance to travel all the unvisited cities (MST heuristic used here) + nearest distance from an unvisited city to the start city. Note that this is an admissible heuristic function.
This hurestic function is computationally very heavy, I used the azure cloud to run it on few of the smaller data sets.

The hw4_wrapper.py script encloses greedy and genetic algorithm execution. 
The utilities file has common functionalities like calculating distance matrix, reading input files, calculating tour lengths, etc.

Data folder has all the input files containing list of cities along with their coordinates. These files belong to the DIMACS dataset.

Below is the graph depicting time taken for each of the algorithms to execute:
<img src="https://github.com/shantanuspark/pathFindingAlgorithmAnalysis/blob/master/GreedyVsGenetic.jpg" />

Below graph depicts the tour lengths of greedy vs genetic algorithm. 
<img src="https://github.com/shantanuspark/pathFindingAlgorithmAnalysis/blob/master/GreedyVsGeneticTourLength.jpg" />
If the genetic algorithm was kept to run longer the tour lengths could have improved substantially.

Below image shows the tour lengths of a*, greedy and genetic algorithm on smaller self curated data sets.
<img src="https://github.com/shantanuspark/pathFindingAlgorithmAnalysis/blob/master/analysisOnSelfGeneratedData.jpg" />
Since the hurestic function used for a* is  O((n^2) * log(n)), it takes very long to run on big datasets.

Finally, below are the results of execution for each of the data file:
<img src="https://github.com/shantanuspark/pathFindingAlgorithmAnalysis/blob/master/result.JPG" />
