import networkx as nx 
import multiprocessing as mp
import time
import numpy as np
import sys
import osmnx
#Graphml file containing street network Hanko, Finland.
graph_file="data/hanko.graphml"
g=nx.read_graphml(graph_file, node_type=int)

print("graph read")

#Add edge weights based on length
for e in g.edges(data=True):
    e[2]['w']=float(e[2]['length'])

#Function to calculate shortest path between two random points on map. Using seed to keep the paths same for each run. If specific nodes were wanted for start and end points these could be accessed with their OSM id numbers. 
def sp(seed):
	np.random.seed(seed)
	route = nx.shortest_path(g, source=np.random.choice(g.nodes),target=np.random.choice(g.nodes), weight='w')
	return route

#Get number of available cores as argument from batch job script so that number of processes used on pool matches number of cores reserved in batch job script.
print(sys.argv[1], " cores")
with mp.Pool(processes=int(sys.argv[1])) as pool:
	t0 = time.time()
	#Map shortest path function to seeds ranging from 0 to 99 to create 100 paths.
	results = pool.map(sp,range(100))
	print("Time spent on path calculations", time.time()-t0, " seconds")
	
