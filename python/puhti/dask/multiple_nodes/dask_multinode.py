"""
An example of a Python script on how to resample all bands for 4 Sentinel satellite images
in parallel with Dask using several computing nodes in Puhti supercomputer

All the files are worked in parallel with the help of Dask delayed functions, see main()-function.
More info about Python Dask library can be found from:
https://docs.dask.org/en/latest/why.html

Author: Johannes Nyman, CSC
Date: 31.03.2020
"""

import sys
import os
import time
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
from dask import delayed
from dask import compute

### Declare the folder with input sentinel SAFE folders and output folder
image_folder = sys.argv[1]
results_folder = '/scratch/project_2000599/dask_slurm/results'

### This is the specifications of one SLURM job
single_worker = {
    "project" : "project_2000599",
    "queue" : "small",
    "nodes" : 1,
    "cores" : 4,
    "memory" : "12000",
    "time" : "00:30:00",
    "temp_folder" : "/scratch/project_2000599/dask_slurm/temp"
}

## Create a results folder to this location
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

def createSLURMCluster():
    cluster = SLURMCluster(
        queue = single_worker['queue'],
        project = single_worker['project'],
        cores = single_worker['cores'],
        memory = single_worker['memory'],
        walltime = single_worker['time'],
        interface = 'ib0',
        local_directory = single_worker['temp_folder']
    )
    client = Client(cluster)
    print(client)

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

def processImage(image_folder_fp):
    ### This is the function that gets parallellized. This gathers all operations we do for one image

    ## Read image and get a list of opened bands
    list_of_band_files = readImage(image_folder_fp)

    ## Calculate NDVI and save the result file
    list_of_resampled = resampleBands(list_of_band_files)

    ## Get image name and save image
    image_name = os.path.basename(image_folder_fp)
    saveImage(ndvi,image_name)

    return image_name

def main():
    createSLURMCluster()

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
