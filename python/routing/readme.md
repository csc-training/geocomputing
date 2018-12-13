## Testing python routing using igraph and networkx with multiprocessing

* osmnx-graphml.py contains example how to create a graph in graphml format from osm data.
* igraph_parallel.py and nx_parallel.py are examples on how to run shortest path analysis with igraph and networkx in parallel with multiprocessing module.
* batch_igarph.sh and batch_nx.sh files are batch job files for submitting the shortest paths scripts to batch job system in Taito.
* Creating graphml file from osm data with osmnx requires a lot of memory as osmnx uses networkx graphs. Downloading from overpass api is suitable for only smaller areas. Downloading whole Finland graph took 19 hours in our tests. 
* Memory consumption increases with parallelisation, but not by much
* Parallelisation done within one node (=up to 16 or 24 cores depending on node type, 256GB memory, 1.5TB in hugemem queue, see Taito userguide for details about different node types and queues)

Time and memory consumption for shortest paths analysis on whole Finland street network from OSM using igraph.

| Cores	 |Wall clock (min:s)|Time on pathfinding (min:s)|Mem (GB)|
| ------ |------------------|-----------------------|--------|
| 1|14:01|11:48|7.35|
| 4|5:39|3:27|8.27|
| 10|3:43|1:31|10.05|

Time and memory consumption for shortest paths analysis on Helsinki street network using networkx

| Cores  |Wall clock (min:s)|Time on pathfinding (min:s)|Mem (GB)|
| ------ |------------------|-----------------------|--------|
| 1|5:01|3:51|2.39|
| 4|4:35|1:08|3.11|
| 10|1:25|0:30|4.38|


