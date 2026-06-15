"""
A simple example Python script how to calculate contours for three DEM files
in parallel with the multiprocessing library.

All the files are working in parallel with the help of a multiprocessing Pool, see main()-function.
More info about Python multiprocessing library can be found from:
https://sebastianraschka.com/Articles/2014_multiprocessing.html

Author: Kylli Ek, CSC

"""

from multiprocessing import Pool
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
    with open("../mapsheets_URLs.txt") as f:
        files = [line.strip() for line in f if line.strip()]

        ## Create a pool of workers and run the function processImage for each filepath in the list
        pool = Pool(parallel_processes)
        pool.map(processFile, files)


if __name__ == "__main__":
    ## This part is the first to execute when script is ran. It times the execution time and runs the main function
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")
