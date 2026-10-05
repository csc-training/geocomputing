"""
An example Python script how to calculate contours for 1 DEM file using just 1 process.

Author: Kylli Ek, CSC

"""
import os
from pathlib import Path
from xrspatial import contours
import numpy as np
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
    base_folder = os.path.join(os.sep, 'scratch', 'project_2020458', 'students', os.environ.get('USER'), 'geocomputing', 'python', 'roihu', '00_interactive')
    os.chdir(base_folder)
    # Run the process for the first file
    with open("../mapsheets.txt") as f:
        first_file = f.readline().strip()        
        processFile(first_file)


if __name__ == "__main__":
    ## This part is the first to execute when script is ran. It times the execution time and runs the main function
    start = time.time()
    main()
    end = time.time()
    print(f"Script completed in {time.time() - start:.1f} seconds")