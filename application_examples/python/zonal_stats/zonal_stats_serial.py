"""
A simple example Python script for zonal_stats Python function.
https://pythonhosted.org/rasterstats/

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

def main():
    print(datetime.now().time())
    # Read data
    zones = geopandas.read_file(zones_file) 
    # Uncomment next 3 rows, if you need to read the file from disk.
    # zonal_stats does not directly work with rasterio opened file, but needs data and transformation variables     
    raster = rasterio.open(raster_file)
    affine = raster.transform
    array = raster.read(1)

    results = zonal_stats(zones.geometry, array, affine=affine, stats=statistics)
    # Use this if raster data is not read to memory   
    #results = zonal_stats(zones.geometry, raster_file, stats=statistics)
        
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


