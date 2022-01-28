"""
A simple example Python script for parallization of zonal_stats Python function with multiprocessing.
https://pythonhosted.org/rasterstats/

zonal_stats calculates statistics for each zone (=polygon) separately, so it is easy to parallelize
with deviding zones to different cores with multiprocessing map() function.

More info about Python multiprocessing library can be found from:
https://docs.python.org/3/library/multiprocessing.html
https://www.machinelearningplus.com/python/parallel-processing-python/

Some notes about input datasets:
Raster:
* If all zones together cover almost all raster data and the raster data is not too big, then the fastest is to read raster dataset to memory 
in the beginning of the script. Just make sure to reserve enogh memory. This causes also least disk readings and is in general the preferred way.
* If the zones cover only some part raster data or if the raster is too big for memory, then direct read from disk might be better. 
See the comments in script, how to modify the code to read directly from disk. If reading data from disk, make sure that the raster has a format that can be paritally read (for example GeoTiff) and that it is has inner tiling (https://gdal.org/drivers/raster/gtiff.html -> TILED) for optimal reading.
In this case, consider also moving the raster to local disk on the computing node:
https://docs.csc.fi/computing/disk/#compute-nodes

Author: Elias Annila, Kylli Ek, CSC
Date: 27.01.2022
"""

from multiprocessing import Pool
from rasterstats import zonal_stats
import geopandas
import rasterio
import time


#input zones file
zones_file = "zones.shp"
#output zonal stats file
zonal_file = "/scratch/project_2000599/python_multiprocessing_rasterstats/zonal_stats.shp"
#Raster you want to use to compute zonal stastics from, CORINE 2018
raster_file = '/appl/data/geo/mml/dem10m/dem10m_direct.vrt'
# Statistics calculated for each zone
statistics = ['count', 'min' ,'mean', 'max','majority']        

# This works inside one node in Puhti, so max 40.
parallel_processes = 4
    
# The task for one worker
def calculate_n(n):
    return zonal_stats(zones.at[n,'geometry'], data_array, affine=affine, stats=statistics)[0]
    # Use this if raster data is not read to memory in the main function
    #return zonal_stats(zones.at[n,'geometry'], raster_file, stats=statistics)[0]    

def main():
    print(datetime.now().time())
    # Read data
    # Worker function needs access to data, so these need to be global variables.
    global zones
    zones = geopandas.read_file(zones_file) 
    # Uncomment next 5 rows, if you need to read the file from disk.
    # zonal_stats does not directly work with rasterio opened file, but needs data and transformation variables 
    global data_array
    global affine      
    raster = rasterio.open(raster_file)    
    affine = raster.transform
    data_array = raster.read(1)

    # Create a sequence of numbers for each zone
    n = range(0, len(zones))
    
    # Create a pool of workers and run the function calculate_n for each zone
    # map() function creates in background batches
    # Often the default batch size is likely good,
    # but if the zones have very different sizes,
    # then it might be good to manually set smaller batch size (15 here).
    pool = Pool(parallel_processes)
    results = pool.map(calculate_n, n, 15)
    
    # Close the pool
    pool.close()    
        
    # Join the results back to geopandas dataframe
    for stat in statistics:
        results_as_list = [d[stat] for d in results]
        zones[stat] = results_as_list  
        
    # Write the results to file
    zones.to_file(zonal_file)

if __name__ == '__main__':
    t0 = time.time()
    main()	
    t1 = time.time()
    total = t1-t0
    print(datetime.now().time())
    print("Everything done, took: " + str(round(total, 0))+"s")


