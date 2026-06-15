"""
An example Python script how to calculate contours for three DEM files
in parallel with the dask.

All the files are working in parallel with the help of Dask delayed functions, see main()-function.
More info about Python Dask library can be found from:
https://docs.dask.org/en/latest/why.html

Author: Kylli Ek, CSC

"""

from dask import delayed
from dask import compute
from pathlib import Path
from xrspatial import contours
import numpy as np
import os
import rioxarray  
import time
import xarray as xr

def processFile(file_path):
    print(f"\n {file_path} started")
    # Open file with xarray
    dem = xr.open_dataarray(file_path, engine="rasterio")
    
    # Xarray adds third dimension, drop it.
    dem = dem.squeeze("band", drop=True)   
    
    # Calculate contours
    lines = contours(dem, levels=np.arange(0, 1300, 100), return_type="geopandas")
    
    # Save output file
    output_filename = Path(file_path).stem + ".gpkg"
    lines.to_file(output_filename, driver="GPKG")
    
    print(f" {file_path} done\n")


def main():
        
    ## How many parallel processes do we want to use
    ## Take all that were reserved from batch job
    parallel_processes = len(os.sched_getaffinity(0))

    ## This list hosts the delayed functions which are then ran with compute()
    list_of_delayed_functions = []

    # Run the process for the all the files
    with open("../../mapsheets_URLs.txt") as f:
        files = [line.strip() for line in f if line.strip()]
        for file in files:
            ### add delayed processFile function for one file to a list instead of running the process directly
            list_of_delayed_functions.append(delayed(processFile)(file))

    ## After constructing the Dask graph of delayed functions, run them with the resources available
    compute(list_of_delayed_functions)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")
