from rasterstats import zonal_stats
import time
import fiona
import multiprocessing as mp
from shapely.geometry import mapping, shape

#input zones
zone_f = "zones.shp"
#output zonal stats
zonal_f = "zonal_stats.shp"
#Raster you want to use to compute zonal stastics from.
vrt = "dem2m.vrt"

statistics = ['count', 'min' ,'mean', 'max','median']

#yields n sized chunks from list l (used for splitting task to multiple processes)
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


#calculates zonal stats and add results to a dictionary
def worker(z,vrt,d):	
	z_stats = zonal_stats(z,vrt, stats=statistics)	
	for i in xrange(0,len(z_stats)):
		d[z[i]['id']]=z_stats[i]

#write output polygon
def write_output(zones, zonal_f,d):
	#copy schema and crs from input and add new fields for each statistic			
	schema = zones.schema.copy()
	crs = zones.crs
	for stat in statistics:			
		schema['properties'][stat] = 'float'
		
	with fiona.open(zonal_f, 'w', 'ESRI Shapefile', schema, crs) as output:
		for elem in zones:
			for stat in statistics:			
				elem['properties'][stat]=d[elem['id']][stat]
			output.write({'properties':elem['properties'],'geometry': mapping(shape(elem['geometry']))})
def main():
	with fiona.open(zone_f) as zones:
		jobs = []

		#create manager dictionary (polygon ids=keys, stats=entries) where multiple processes can write without conflicts
		man = mp.Manager()	
		d = man.dict()	

		#split zone polygons into 10 chunks for parallel processing and call worker() for each. Adjust 10 to be number of cores you want to use for optimal performance.
		split = chunks(zones, len(zones)/10)
		for z in split:
			p = mp.Process(target=worker,args=(z, vrt,d))
			p.start()
			jobs.append(p)

		#wait that all chunks are finished
		[j.join() for j in jobs]

		write_output(zones,zonal_f,d)		
		
if __name__ == '__main__':
	t0 = time.time()
	main()	
	t1 = time.time()
	total = t1-t0
	print "Everything done, took: ", str(total)+"s" 
