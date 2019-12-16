"""
An example how to use Dask and Xarray to process Sentinel images in parallel. This example calculates NDVI for each image.

Author: Johannes Nyman, CSC
Date: 16.12.2019
"""

import os
import xarray as xr
import time
from dask import delayed
from dask import compute

### This import exists in a another python file called rasterio_to_xarray.py
### It is downloaded from here https://github.com/robintw/XArrayAndRasterio/blob/master/rasterio_to_xarray.py
from rasterio_to_xarray import xarray_to_rasterio

### Declare the folder with input sentinel SAFE folders and output folder
image_folder = r"/scratch/project_2000599/data/sentinel_images/L2A"
output_folder = r"/projappl/project_2000599/dask_test/results"

def readImage(image_folder_fp):

    ### Rather than figuring out what the filepath inside SAFE folder is, this is just finding the red and nir files with correct endings
    for subdir, dirs, files in os.walk(image_folder_fp):
        for file in files:
            if file.endswith("_B04_10m.jp2"):
                red_fp = os.path.join(subdir,file)
            if file.endswith("_B08_10m.jp2"):
                nir_fp = os.path.join(subdir,file)

    ### Read the red and nir band files to xarray and with the chunk-option to dask
    red = xr.open_rasterio(red_fp, chunks={'band': 1, 'x': 1024, 'y': 1024})
    nir = xr.open_rasterio(nir_fp, chunks={'band': 1, 'x': 1024, 'y': 1024})

    ### Scale the image values back to real reflectance values
    red = red /10000
    nir = nir /10000

    ### Print out dimensions, data type etc information
    print(red.variable.data)
    print(nir.variable.data)

    return [red,nir]

def calculateNDVI(list_of_bands):
    ### This function calculates NDVI and saves the file

    ## Repopulating the list back to variables
    red = list_of_bands[0]
    nir = list_of_bands[1]

    ## NDVI calculation for all pixels where red or nir != 0
    ndvi = xr.where((nir ==0)  & (red==0), 0, (nir - red) / (nir + red))

    return ndvi

def processImage(image_folder_fp):
    ### This is the function that gets parallellized. This gathers all operations we do for one image

    ## Read image and get a list of opened bands
    list_of_bands = readImage(image_folder_fp)

    ## Calculate NDVI and save the result file
    ndvi = calculateNDVI(list_of_bands)

    ## Get image name and save image
    image_name = os.path.basename(image_folder_fp)
    saveImage(ndvi,image_name)

    return image_name

def saveImage(ndvi,image_name):
    ## Create the output filename and save it with using a function xarray_to_rasterio from a separate python file
    output_file = image_name.replace(".SAFE", "_NDVI.tif")
    xarray_to_rasterio(ndvi, os.path.join(output_folder, output_file))


def main():

    ## This list hosts the delayed functions which are then ran with compute()
    list_of_delayed_functions = []

    ## Iterate through the Sentinel SAFE folders
    for directory in os.listdir(image_folder):
        folder_path = os.path.join(image_folder, directory)
        if os.path.isdir(folder_path):
            print(folder_path)
            ### add delayed processImage function for one image to a list  
            list_of_delayed_functions.append(delayed(processImage)(folder_path))

    ## After constructing the Dask graph of delayed functions, run them with the resources available
    compute(list_of_delayed_functions)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")
