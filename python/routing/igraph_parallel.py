import igraph 
import multiprocessing as mp
import time
import sys

#Graphml file containing street network from Hanko, Finland.
#graph_file="data/hanko.graphml"
g =  igraph.read(graph_file)

#Create edge weights based on length
for e in g.es:
	e['weight']=float(e['length'])

#Create "size" amount of (start, end) pairs in list like such: [(s1,e1),(s2,e2)...] where start and end are vertex indices
size=500
args= [(int(len(g.vs)*(1/size)*i),int(len(g.vs)*(1/size)*(i+1)-1)) for i in range(0,size)]


#Function to calculate shortest path and in this case just return sum of edge weights. (You can also get path length directly from igraph with igraph.shortest_paths(), but usually you'd probably also want the actual path.
def sp(start,end):
	path=g.get_shortest_paths(start, to=end, weights='weight',output="epath")
	path_len=[g.es[e]['weight'] for e in path[0]]
	return sum(path_len)

#Get number of cores from batch job script as argument, so number of processes used here matches the reserved number of cores
print(sys.argv[1], " cores")

#Create multiprocessing pool and map shortest path calculations for each start, end pair to the pool.
with mp.Pool(processes=int(sys.argv[1])) as pool:
	t0 = time.time()
	results = pool.starmap(sp, args)
	print("Time spent on path calculations", time.time()-t0, " seconds")
	print(sum(results))
