"""
A simple example Python script how to contours for three DEM files
in parallel with the joblib library.

All the files are working in parallel with the help of a joblib Parallel jobs, see main()-function.
More info about Python joblib library can be found from:
https://joblib.readthedocs.io/en/latest/parallel.html

Author: Kylli Ek, CSC

"""

from joblib import Parallel, delayed
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

    # Run the process for the all the files
    with open("../mapsheets.txt") as f:
        files = [line.strip() for line in f if line.strip()]
        
        ## Start a Parallel job that gives one path from the list to a worker process
        Parallel(n_jobs=parallel_processes)(
            delayed(processFile)(file) for file in files
        )        


if __name__ == "__main__":
    ## This part is the first to execute when script is ran. It times the execution time and rans the main function
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {time.time() - start:.1f} seconds")