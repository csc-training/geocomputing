# Change coordinate system of many files with GDAL and bash script.

**GDAL** provides many useful tools. In this example, we will reproject the coordinate system of multiple files in a folder, and add overviews to the same files. 
We do not use R nor Python, but GDAL commands from a simple Linux bash script.

## Interactive working 
* Start an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/)
```
sinteractive -i
```
* Open the [gdal.sh](gdal.sh) file with nano in Puhti and fix the path of output file and save the file.
* Load [GDAL module](https://docs.csc.fi/apps/gdal/)
```
module load gcc/9.1.0 gdal
```
* Check the original file with gdalinfo. What is the coordinate system? Are the files tiled? Do they have overviews?
```
gdalinfo /appl/data/geo/mml/dem10m/etrs-tm35fin-n2000/W3/W33/W3333.tif
```
* Change the permissions of gdal.sh, so that it can be executed: 
```
chmod 770 gdal.sh
```
* Run the script: 
```
./gdal.sh
```
* Check the result file with `gdalinfo`. What is the coordinate system? Are the files tiled? Do they have overviews?
* [gdal_batch_job.sh](gdal_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which modules are used?

## Simple batch job
For simple 1 core batch job, use the same bash-script as for interactive working.

* Run the script as batch file: 
```
sbatch gdal_batch_job.sh
```
* `sbatch` prints out a job id, use it to check state and efficiency of the batch job. Did you reserve a good amount of memory?
```
seff <jobid>
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. 
* Check that you have new GeoTiff files in working folder.
* Check the resources used in another way. 
```
sacct -j <jobid> -o elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in job.
	- AllocCPUS – how many CPUs were reserved
