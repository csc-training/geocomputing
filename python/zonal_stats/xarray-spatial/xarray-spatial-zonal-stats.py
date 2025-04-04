#!/usr/bin/env python
# coding: utf-8
# Created 13.3.2025, by Kylli Ek, CSC

import geopandas as gpd
from geocube.api.core import make_geocube
from xrspatial import zonal_stats
import rioxarray
from dask.distributed import Client, Lock
import os, time

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

def main():
    # Get the number of workers
    no_of_workers = len(os.sched_getaffinity(0))
    # Create Dask Client for parallel processing
    client = Client(n_workers=no_of_workers)

    # Read the raster file, to read as Dasked backed Xarray DataArray
    # Notice the use of `chunks=True`.
    dem10m = rioxarray.open_rasterio(raster_file, chunks=True) 
    # Crop the raster file to processing area, leave out if you want to process the whole file
    dem10m_clip = dem10m.rio.clip_box(minx=x_min, miny=y_min, maxx=x_max, maxy=y_max)

    # Read the vector polygons, leave out bbox, if you want to process the whole file
    polygons = gpd.read_file(polygons_file , layer="KASVULOHKO", bbox=bbox_3067)
    polygons['ID'] = polygons.PERUSLOHKOTUNNUS.astype(int)

    # Create Xarray DataArray similar to the raster data
    out_grid = make_geocube(
        vector_data=polygons,
        measurements=["ID"],
        like=dem10m_clip
    )

    # Write the rasterized polygons to the disk, so that Dasked backed Xarray DataArray could be created of them.
    out_grid["ID"].rio.to_raster("fields.tif", lock=Lock(name="rio"))

    # Read the rasterized polygons back in as Dasked backed Xarray DataArray
    fields = rioxarray.open_rasterio("fields.tif", chunks=True)

    # Caclulate the zonal statistics
    zonal_stats_values = zonal_stats(fields[0], dem10m_clip[0], stats_funcs=['mean']).compute()

    # Join the results back to the original zones data
    polygons_result  = polygons.merge(zonal_stats_values.compute(), left_on='ID', right_on='zone', how='left')

# With Dask, it is important to use the main function
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")
