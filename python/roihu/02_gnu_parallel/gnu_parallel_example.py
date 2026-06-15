"""
An example Python script how to calculate contours for one DEM file

Author: Kylli Ek, CSC

"""
from pathlib import Path
from xrspatial import contours
import numpy as np
import rioxarray  
import sys
import time
import xarray as xr

### The filepath to the input file is an input argument to the script
file_path = sys.argv[1]

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
    
    print(f"{file_path} done")


def main():
    processFile(file_path)

if __name__ == "__main__":
    ## This part is the first to execute when script is ran. It times the execution time and runs the main function
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {str(end - start)} seconds")
