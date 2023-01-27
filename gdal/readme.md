# Using commandline tools with bash scripts and batch jobs

GDAL reprents here a commandline tool that is used via Linux bash scripts. The example includes:

* A basic serial batch job, where several files are handled in a for loop, one after the other. Only 1 core is used.
* Parallel batch job, where different files are handled in parallel with GNU-parallel. Up to one node can be used, in Puhti that is up to 40 cores.

GDAL includes many other useful [commanline tools](https://gdal.org/programs/index.html), which usually are very efficient. In this example, we will reproject the coordinate system of multiple files in a folder, and add overviews to the same files. We do not use R nor Python, but GDAL commands from a simple Linux bash script.

## Interactive working 
With `gdalinfo` and `ogrinfo` it is often helpful to check the files, this is a light-weight task, so it can be done from login-node without interactive session.

* Load [GDAL module](https://docs.csc.fi/apps/gdal/)
```
module geoconda
```
* Check a file with `gdalinfo`. What is the coordinate system? Are the files tiled? Do they have overviews?
```
gdalinfo /appl/data/geo/mml/dem10m/2019/W3/W33/W3333.tif
```

## Serial batch job

* [gdal_serial.sh](gdal_serial.sh) includes GDAL commands to be executed. For handling several files a for loop is used.
* [gdal_batch_job_serial.sh](gdal_batch_job_serial.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which modules are used?

* Change file permission to be executable:
```
chmod 770 gdal_serial.sh
```

* Run the script as batch file: 
```
sbatch gdal_batch_job_serial.sh
```
* Check that you have new GeoTiff files in working folder. Check the result file with `gdalinfo`. What is the coordinate system? Are the files tiled? Do they have overviews?

* `sbatch` prints out a job id, use it to check state and efficiency of the batch job. Did you reserve a good amount of memory?
```
seff <jobid>
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. 

* Check the resources used in another way. 
```
sacct -j <jobid> -o elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in job.
	- AllocCPUS – how many CPUs were reserved

## Parallel job

* [gdal_parallel.sh](gdal_parallel.sh) includes GDAL commands to be executed for one file. The for loop is removed.
* [gdal_batch_job_parallel.sh](gdal_batch_job_parallel.sh). How many cores are reserved? How much memory? Which modules are used? GNU parallel is used for handling several files. In this way max one node (= 40 cores) can be used. If even more is needed, see ["Workflow for many small, independent runs" tutorial](https://docs.csc.fi/support/tutorials/many/) how to combine this with array jobs.

* Run the script as batch file: 
```
sbatch gdal_batch_job_parallel.sh
```
* Check the parallel batch job results with seff.
