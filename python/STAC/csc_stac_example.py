#!/usr/bin/env python
# coding: utf-8

# This example shows how to use STAC, dask and xarray via Python script. 
# If new to STAC, see the STAC_CSC_example.ipynb for longer explanation how STAC works.
# In this example, we will search and download data through a STAC Catalog and process it using Dask and Xarray. 
# We will use Sentinel-1 data stored at FMI to compute a mean value of vv_mean for one month. The result will be saved to a new GeoTiff file.

import requests
import stackstac
from dask.distributed import Client, Lock
import pystac_client
import rioxarray
import sys
import os

# Settings
STAC_URL = "https://paituli.csc.fi/geoserver/ogc/stac/v1"
collection = 'sentinel_1_11_days_mosaics_at_fmi'
time_filter="2021-03-01/2021-03-31"
asset = 'mean_vv'
output_file = os.path.join(os.getcwd(), "sentinel1_mean_vv.tif")

# Use as many workers as you have available cores
no_of_workers = len(os.sched_getaffinity(0))

# To overcome a current bug, rewrite requests to https. Needed only with Paituli STAC.
def change_to_https(request: requests.Request) -> requests.Request: 
    request.url = request.url.replace("http:", "https:")
    return request

def find_items_from_stac():
    catalog = pystac_client.Client.open(STAC_URL, request_modifier=change_to_https)
    search_bbox = catalog.search(
        collections=[collection],
        datetime=time_filter
    )
    return search_bbox.item_collection()

def main():

    # Create Dask client
    # Because STAC+xarray analysis is usually slowed down by data download speed, then it is good to use 1 core per worker.
    # If you have computationally heavy analysis, this could be changed to several cores per worker.
    client = Client(n_workers=no_of_workers)

    item_collection = find_items_from_stac()

    # Use the `stackstac` library to convert item collection to Xarray DataArray. 
    cube = stackstac.stack(
        items=item_collection,
        assets=[asset],
        #chunksize=(-1,1,2046,2046),
        epsg=3067
    ).squeeze() 
    
    # Create new data cube for the mean value. 
    mean = cube.mean("time", keep_attrs=True)

    # Compute and save the result
    mean_ndvi_tiff = mean.rio.to_raster(
        output_file,
        lock=Lock(name="rio", client=client),
        tiled=True,
    )
   
    # Close Dask cluster
    client.close()

# With Dask, it is important to use the main function
if __name__ == "__main__":
    main()
    print("Analysis ready")
