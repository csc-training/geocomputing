"""
An example Python script how to calculate NDVI for three Sentinel satellite images
in parallel with multiple HPC nodes with the Dask-Jobqueue: https://jobqueue.dask.org/en/latest/index.html.

All the files are working in parallel with the help of Dask delayed functions, see main()-function.

The basic idea of Dask-Jobqueue is that from this script more SLURM jobs are started that are used for Dask workers.
With several SLURM jobs it is possible to use several HPC nodes that is not possible with other Python parallelization options presented in this Github repo.

Author: Johannes Nyman, Kylli Ek, Samantha Wittke CSC

"""

import os
import sys
import rasterio
import time
from dask_jobqueue import SLURMCluster
from dask.distributed import Client, print #Dask print enables seeing worker printouts from main script
from dask import delayed
from dask import compute

# The folder with input sentinel SAFE folders 
image_folder = sys.argv[1]

# CSC project name for SLURMCluster
project_name = sys.argv[2]

def createSLURMCluster():
    # The number of SLURM jobs
    # Practically, how many nodes you want to use
    number_of_jobs = 2

    # Next, limits and settings for ONE SLURM job. 
    
    # Number of cores per SLURM job. 
    # In bigger analysis this has to fit to one HPC node, so in Puhti max 40 cores.  

    no_of_cores = 2 
    
    # Here no_of_cores is also used as number of workers (processes) per SLURM job, but number of workers could also be smaller, but not bigger.
    
    # The memory per SLURM job, so all workers of one SLURM job together. Count with at least 6 Gb per worker, possibly more.
     
    # Pay attention to the time option here, especially if you have more delayed functions (=files here) than workers.
    # The worker lifetime should be long enough to handle all delayed functions.
    
    # For futher details see: https://jobqueue.dask.org/en/latest/configuration-setup.html
    
    cluster = SLURMCluster(
        queue="small",
        account=project_name,
        cores=no_of_cores,
        processes=no_of_cores,
        memory="12G",
        walltime="00:10:00",
        interface="ib0"
    )

    cluster.scale(number_of_jobs)
    client = Client(cluster)
    print(cluster.job_script())
    print(client)


def readImage(image_folder_fp):
    print("Reading Sentinel image from: %s" % (image_folder_fp))

    ### Rather than figuring out what the filepath inside SAFE folder is, this is just finding the red and nir files with correct endings
    for subdir, dirs, files in os.walk(image_folder_fp):
        for file in files:
            if file.endswith("_B04_10m.jp2"):
                red_fp = os.path.join(subdir, file)
            if file.endswith("_B08_10m.jp2"):
                nir_fp = os.path.join(subdir, file)

    ### Read the red and nir (near-infrared) band files with Rasterio
    red = rasterio.open(red_fp)
    nir = rasterio.open(nir_fp)

    ### Return the rasterio objects as a list
    return red, nir


def calculateNDVI(red, nir):
    print("Computing NDVI")
    ### This function calculates NDVI from the red and nir bands

    ## Read the rasterio objects pixel information to numpy arrays
    red = red.read(1)
    nir = nir.read(1)

    ### Scale the image values back to real reflectance values (sentinel pixel values have been multiplied by 10000)
    red = red / 10000
    nir = nir / 10000

    ### the NDVI formula
    ndvi = (nir - red) / (nir + red)
    return ndvi


def saveImage(ndvi, sentinel_image_path, input_image):
    ## Create an output folder to this location, if it does not exist
    outputdir = "output"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    ## Create output filepath for the image. We use the input name with _NDVI end
    output_file = os.path.join(
        outputdir, os.path.basename(sentinel_image_path).replace(".SAFE", "_NDVI.tif")
    )
    print(f"Saving image: {output_file}")
    ## Copy the metadata (extent, coordinate system etc.) from one of the input bands (red)
    metadata = input_image.profile
    ## Change the data type from integer to float and file type from jp2 to GeoTiff
    metadata.update(dtype=rasterio.float64, driver="GTiff")
    ## Write the ndvi numpy array to a GeoTiff with the updated metadata
    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(ndvi, 1)


def processImage(sentinel_image_path):
    ### This function processes one image (read, compute, save)

    ## Read the image and get rasterio objects from the red nir bands
    red, nir = readImage(sentinel_image_path)

    ## Calculate NDVI and get the resulting numpy array
    ndvi = calculateNDVI(red, nir)

    ## Write the NDVI numpy array to file to the same extent as the red input band
    saveImage(ndvi, sentinel_image_path, red)


def main():

    createSLURMCluster()
    
    ## This list hosts the delayed functions which are then ran with compute()
    list_of_delayed_functions = []

    ## Iterate through the Sentinel SAFE folders
    for directory in os.listdir(image_folder):
        folder_path = os.path.join(image_folder, directory)
        if os.path.isdir(folder_path):
            print(folder_path)
            ### add delayed processImage function for one image to a list instead of running the process directly
            list_of_delayed_functions.append(delayed(processImage)(folder_path))

    ## After constructing the Dask graph of delayed functions, run them with the resources available
    compute(list_of_delayed_functions)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Script completed in " + str(end - start) + " seconds")
