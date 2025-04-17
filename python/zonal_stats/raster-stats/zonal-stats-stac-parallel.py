# coding: utf-8
"""
A simple example Python script for parallization of zonal_stats Python function with dask if using time-series rasters from STAC.

Rasterstats calculates statistics only for one 2D raster, so in case of time-series or several bands, each timestep or band has to be calculated separately.
In this script the parallelization is done between different timesteps and bands. The files are found using STAC.

Technically for parallization are used Dask Delayed functions.

See also:
* https://github.com/csc-training/geocomputing/tree/master/python/STAC longer STAC example
* https://github.com/csc-training/geocomputing/tree/master/python/puhti for parallelization with Python in HPC.

Author: Kylli Ek (CSC), Riku Putkinen (Arbonaut)
Date: 15.04.2025
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import pyproj
import dask
import rasterstats
import stackstac
import pystac_client
import time


# Set the processing area in WGS-84 for STAC
long_min = 21.0
lat_min = 60.5
buffer = 0.5
long_max = long_min + buffer
lat_max = lat_min + buffer
bbox_wgs = [long_min, lat_min, long_max, lat_max]

# Set the processing area in Finnish coordinates system EPSG:3067, the native projection of the polygons
x_min, y_min, = pyproj.Proj("EPSG:3067")(long_min, lat_min)
x_max, y_max  = pyproj.Proj("EPSG:3067")(long_max, lat_max)
bbox_3067 = (x_min, y_min, x_max, y_max)

# Polygons file
zones_file = '/appl/data/geo/ruokavirasto/kasvulohkot/2020/LandUse_ExistingLandUse_GSAAAgriculturalParcel.gpkg'
# If running the code outside Puhti, get the data from Paituli.
# zones_file = 'https://www.nic.funet.fi/index/geodata/ruokavirasto/kasvulohkot/2020/LandUse_ExistingLandUse_GSAAAgriculturalParcel.gpkg'

# Read the vector polygons
def read_polygons():
    # Leave out bbox, if you want to process the whole file
    zones = gpd.read_file(zones_file , layer="KASVULOHKO", bbox=bbox_3067)
    return zones

# Find the relevant raster files using STAC and create Xarray DataArray 
def get_raster_stack():
    # Define STAC endpoint and open the catalog
    URL = "https://paituli.csc.fi/geoserver/ogc/stac/v1"
    catalog = pystac_client.Client.open(URL)
    
    # Search for relevant STAC items
    search = catalog.search(
        bbox = bbox_wgs,
        collections = "sentinel_2_11_days_mosaics_at_fmi",
        datetime = "2023-07-01/2023-07-31"
    )
    
    # Create Xarray DataArray from the search results
    # At this point no data is actually read to memory
    # Data is read to memory by Dask as the process will actually need the data.
    stack = stackstac.stack(
        items=search.item_collection(),
        assets=['b02', 'b03', 'b04'],
        bounds=bbox_3067,
        epsg=3067,
        resolution=10
    ).squeeze()

    return stack

# Define DELAYED function to calculate zonal statistics for one raster, in this case one timestamp and one band.
@dask.delayed
def stats_for_day_band(vector_df, band, band_title, date_str):

    # Read data to memory, for this specific date and band
    band_data = band.compute().data

    # Calcuate zonal statistics
    stats = rasterstats.zonal_stats(vector_df.geometry,
                                    band_data,
                                    affine=band.transform,
                                    stats="mean",
                                    all_touched=True)
    
    # Convert the results to Pandas DataSeries, to have them in suitable format for joining back to the polygons dataframe
    stats_series = pd.Series(
        # Get the calculated mean values out of the dictionaries
        data=[item["mean"] for item in stats],
        index=vector_df.index,
        name=f"S2_{date_str}_{band_title}_MEAN"
    )
    
    return stats_series 

# Prepare delayed functions for each timestep and band
def calculate_statistics(zones, stack):
    # Calculate zonal statistics for all bands and timesteps
    s2_11_d_stats = []

    # Loop through time dimension
    for t in stack:
        date_str = np.datetime_as_string(t.time.values, unit="D")

        # Loop through bands
        for band in t:
            band_title = str(band.title.values).upper()
            s2_11_d_stats.append(stats_for_day_band(zones, band, band_title, date_str))

    return s2_11_d_stats

def main():
    # Read the polygons
    zones = read_polygons()
    
    # Create Xarray datacube of rasters
    stack = get_raster_stack()

    # Prepare delayed functions for each timestep and band
    s2_11_d_stats = calculate_statistics(zones, stack)
    
    # Calculate the statistics
    # First here actual raster data is read and the analysis is started.
    stats = dask.compute(*s2_11_d_stats)
    
    # Combine all the statistics into a single DataFrame
    stats_df = pd.concat(stats, axis=1)

    # Join the results to the original polygons dataframe
    training_data_all_stats = pd.concat([zones, stats_df], axis=1)

# With Dask, it is important to use the main function
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {str(end - start)} seconds")