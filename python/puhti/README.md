# Overview

These are examples on how to run **Python processes in Puhti** with different parallelisation methods. 
The examples are about calculating NDVI (Normalized Difference Vegetation Index) from the Sentinel red and near infrared bands.
The reading, writing and calculation of NDVI are identical in the examples (with the exception of the Dask example) 
and only the method of parallelisation changes (the code in the main function)

Examples included here are

* **single core job**
* **array job**
* **multiprocessing library** (parallel job)
* **joblib library** (parallel job)
* **dask and xarray libraries** (parallel job)

# Scripts

You can download these scripts to **Puhti** into a location of your choice with the command

`git clone https://github.com/csc-training/geocomputing.git`

# Data 

These examples use a set of three **Sentinel L2A images** from southern Finland. You can download the set to **Puhti** from **Allas** with the command:

`wget <ALLAS-URL>`

and unzip it to your project's scratch folder

`unzip <ZIP-NAME> -d /scratch/<YOUR-PROJECT>`

# Running the examples 

You can submit these jobs to Puhti by 

* Navigating to the directory of an example
* Changing the batch job script (the .sh file) to include your project's number
* Running `sbatch <THE-EXAMPLES-BATCH-JOB-SCRIPT>`

See the difference in job execution times for the different jobs after completion with the command `seff <JOB-ID>`

# Example benchmarks 

| Example         | Jobs | CPU cores / job | Time (min) | CPU efficiency |
|-----------------|------|-----------------|------------|----------------|
| single core     | 1    | 1               | 03:23      | 86.70%         |
| multiprocessing | 1    | 3               | 01:05      | 92.31%         |
| joblib          | 1    | 3               | 01:12      | 86.57%         |
| dask            | 1    | 3               | 01:22      | 78.46%         |
| array job       | 3    | 1               |            |                |



