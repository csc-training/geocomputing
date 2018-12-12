## Testing python igraph with multiprocessing

* igraph.Vertex objects can't be passed as arguments with multiprocessing pool (can't pickle). Luckily vertices can be referenced by their index
* Memory consumption doesn't increase significantly with parallelisation
* Parallelisation done within one node (=up to 16 or 24 cores depending on node type, 256GB memory, 1.5TB in hugemem queue, see Taito userguide for details about different node types and queues)

### Time and memory consumption for shortest paths analysis on whole Finland street network from OSM.

| Cores	 |Wall clock (min:s)|Time on pathfinding (min:s)|Mem (GB)|
| ------ |------------------|-----------------------|--------|
| 1|14:01|11:48|7.35|
| 4|5:39|3:27|8.27|
| 10|3:43|1:31|10.05|
