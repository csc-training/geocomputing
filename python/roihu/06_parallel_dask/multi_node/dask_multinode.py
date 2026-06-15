"""
An example Python script how to calculate contours for three DEM files
in parallel with multiple HPC nodes with the Dask-Jobqueue: https://jobqueue.dask.org/en/latest/index.html.

All the files are working in parallel with the help of Dask delayed functions, see main()-function.

The basic idea of Dask-Jobqueue is that from this script more SLURM jobs are started that are used for Dask workers.
With several SLURM jobs it is possible to use several HPC nodes that is not possible with other Python parallelization options presented in this Github repo.

Author: Kylli Ek, CSC

"""


from dask_jobqueue import SLURMCluster
from dask.distributed import Client, print #Dask print enables seeing worker printouts from main script
from dask import delayed
from dask import compute
from pathlib import Path
from xrspatial import contours
import numpy as np
import os
import rioxarray  
import sys
import time
import xarray as xr


# CSC project name for SLURMCluster
project_name = sys.argv[1]

def createSLURMCluster():
    # The number of SLURM jobs
    # Practically, how many nodes you want to use
    number_of_jobs = 2

    # Next, limits and settings for ONE SLURM job. 
    
    # Number of cores per SLURM job. 
    # In bigger analysis this has to fit to one HPC node, so in Roihu max 384 cores.  

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
        memory="4G",
        walltime="00:10:00",
        interface="ib0"
    )

    cluster.scale(number_of_jobs)
    client = Client(cluster)
    print(cluster.job_script())
    print(client)


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
    
    createSLURMCluster()
        
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
