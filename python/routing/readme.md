## Routing using Python igraph or networkx package with multiprocessing

Here you can find example code for doing network routing in Taito with Python igraph or networkx package. For reading the data from OpenStreetMap osmnx package is used. osmnx can create network data needed by networkx directly. For igraph the data has to be save in GraphML format first, and then igraph can read from GraphML. In general igraph is faster and requires less memory, while networkx might be easier to use.

Files:
* osmnx-graphml.py - how to create a graph in GraphML format from OpenStreetMap data.
* igraph_parallel.py and nx_parallel.py - how to run shortest path analysis with igraph and networkx in parallel with multiprocessing module.
* batch_igarph.sh and batch_nx.sh - batch job files for submitting the shortest paths scripts to batch job system in Taito.

Notes:
* Creating GraphML file from OpenStreetMap data with osmnx requires a lot of memory as osmnx uses networkx graphs. Downloading from overpass API is suitable for only smaller areas. Downloading whole Finland graph took 19 hours in our tests. 
* Memory consumption increases with parallelisation, but not by much
* Parallelisation is done within one node, in Taito up to 24 cores and 256GB memory (or 1.5TB in hugemem queue) can be used.

###Test results
Time and memory consumption for shortest paths analysis on whole *Finland* street network from OSM using igraph.

| Cores	 |Wall clock (min:s)|Time on pathfinding (min:s)|Mem (GB)|
| ------ |------------------|-----------------------|--------|
| 1|14:01|11:48|7.35|
| 4|5:39|3:27|8.27|
| 10|3:43|1:31|10.05|

Time and memory consumption for shortest paths analysis on *Helsinki* street network using networkx

| Cores  |Wall clock (min:s)|Time on pathfinding (min:s)|Mem (GB)|
| ------ |------------------|-----------------------|--------|
| 1|5:01|3:51|2.39|
| 4|4:35|1:08|3.11|
| 10|1:25|0:30|4.38|


