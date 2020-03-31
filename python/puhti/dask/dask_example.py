"""
A simple example Python script how to calculate NDVI for three Sentinel satellite images
in parallel with the dask and xarray library

Author: Johannes Nyman, CSC
Date: 31.03.2020
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
image_folder = r"/Users/jnyman/Downloads/sentinel_images"
output_folder = os.path.join(image_folder,"results")

def readImage(image_folder_fp):
    print("Reading Sentinel image from: %s" % (image_folder_fp))

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

    return red,nir

def calculateNDVI(red,nir):
    print("Computing NDVI")
    ### This function calculates NDVI with xarray

    ## NDVI calculation for all pixels where red or nir != 0
    ndvi = xr.where((nir ==0)  & (red==0), 0, (nir - red) / (nir + red))

    return ndvi

def processImage(image_folder_fp):
    ### This is the function that gets parallellized. This gathers all operations we do for one image

    ## Read image and get a list of opened bands
    red,nir = readImage(image_folder_fp)

    ## Calculate NDVI and save the result file
    ndvi = calculateNDVI(red,nir)

    ## Get image name and save image
    image_name = os.path.basename(image_folder_fp)
    saveImage(ndvi,image_name)

    return image_name

def saveImage(ndvi,image_name):
    ## Create the output filename and save it with using a function xarray_to_rasterio from a separate python file
    output_file = image_name.replace(".SAFE", "_NDVI.tif")
    output_path = os.path.join(output_folder, output_file)

    print("Saving image: %s" % output_path)
    xarray_to_rasterio(ndvi,  output_path)

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
