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
Date: 27.01.2022, updated 13.3.2025
"""

from rasterstats import zonal_stats
import geopandas as gpd
import rasterio
import time

# Set the processing area, leave out if you want to process the whole file
x_min = 350000.0
y_min = 6700000.0
buffer = 200000
x_max = x_min + buffer
y_max = y_min + buffer

bbox_3067 = (x_min, y_min, x_max, y_max)

# File paths:
# Raster you want to use to compute zonal stastics from
raster_file = '/appl/data/geo/mml/dem10m/dem10m_direct.vrt'
# If running the code outside Puhti, get the data from Paituli.
# https://www.nic.funet.fi/index/geodata/mml/dem10m/dem10m_direct.vrt

# Polygons file
polygons_file = '/appl/data/geo/ruokavirasto/kasvulohkot/2020/LandUse_ExistingLandUse_GSAAAgriculturalParcel.gpkg'
# If running the code outside Puhti, get the data from Paituli.
# polygons_file = 'https://www.nic.funet.fi/index/geodata/ruokavirasto/kasvulohkot/2020/LandUse_ExistingLandUse_GSAAAgriculturalParcel.gpkg'

# Statistics calculated for each zone
statistics = ['mean']
#statistics = ['count', 'min' ,'mean', 'max','majority']        

def main():
    
    # Read the vector polygons, leave out bbox, if you want to process the whole file
    zones = gpd.read_file(polygons_file , layer="KASVULOHKO", bbox=bbox_3067)

    # zonal_stats does not directly work with rasterio opened file, but needs data and transformation variables     
    with rasterio.open(raster_file) as src:
        # If you want to use the whole raster file, leave out the window part.
        raster = src.read(indexes=1, window=rasterio.windows.from_bounds(x_min, y_min, x_max, y_max, src.transform)) 
        results = zonal_stats(zones.geometry, raster, affine=src.transform, stats=statistics)

    # If you need to read the file from disk.
    # results = zonal_stats(zones.geometry, raster_file, stats=statistics)
    
    #Join the results back to geopandas dataframe        
    for stat in statistics:
        results_as_list = [d[stat] for d in results]
        zones[stat] = results_as_list  
        
if __name__ == '__main__':
    t0 = time.time()
    main()	
    t1 = time.time()
    total = t1-t0
    print("Everything done, took: " + str(round(total, 0))+"s")
