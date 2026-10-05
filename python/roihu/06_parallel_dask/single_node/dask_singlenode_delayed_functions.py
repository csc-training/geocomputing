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

    # Get file list to compute
    with open("../../mapsheets_URLs.txt") as f:
        files = [line.strip() for line in f if line.strip()]

    ## This list hosts the delayed functions which are then ran with compute()
    tasks = [delayed(processFile)(file) for file in files]

    # Processes avoid GDAL thread-safety issues; each worker cleans up on its own
    compute(*tasks, scheduler="processes", num_workers=parallel_processes)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {time.time() - start:.1f} seconds")