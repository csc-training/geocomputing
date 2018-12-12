import networkx as nx 
import multiprocessing as mp
import time
import numpy as np
import sys
import osmnx
#Graphml file containing street network Hanko, Finland.
graph_file="data/helsinki.graphml"

g=nx.read_graphml(graph_file, node_type=int)
#g=osmnx.graph_from_place("Modena,Italy")
print("graph read")

for e in g.edges(data=True):
    e[2]['w']=float(e[2]['length'])



#Function to calculate shortest path and in this case just return sum of edge weights. (You can also get path length directly from igraph with igraph.shortest_paths(), but usually you'd probably also want the actual path.
def sp(seed):
	np.random.seed(seed)
	route = nx.shortest_path(g, source=np.random.choice(g.nodes),target=np.random.choice(g.nodes), weight='w')
	return route

print(sys.argv[1], " cores")
with mp.Pool(processes=int(sys.argv[1])) as pool:
	t0 = time.time()
	results = pool.map(sp,range(100))
	print("Time spent on path calculations", time.time()-t0, " seconds")
	
