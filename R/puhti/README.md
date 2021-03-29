# R Puhti example, calculating contours
This is an example for running R code on CSC's Puhti supercluster as four different job styles: interactive, simple serial, array and parellel. For parallel there are three different options with different R libraries: `snow`, `parallel` and `future`. The interactive style is best for developing your scripts, usually with limited test data. For computationally more demanding analysis you have to use Puhti's batch system for requesting the resources and running your script. 

The contours are calculated based on a geotiff image with `raster` package. The results are saved in Shape format. 

If you have an R script that is ready on your laptop, and now would like to run that in Puhti, you normally need to edit only the paths to files and folders. Sometimes it might be necessary to install [new R libraries](https://docs.csc.fi/apps/r-env-singularity/#r-package-installations).

[Puhti batch job system documentation](https://docs.csc.fi/computing/running/creating-job-scripts/)

Files in this example:
* [mapsheets.txt](mapsheets.txt) file - defines which mapsheets to process. Open the file. How many mapsheets (=files) there is?
* The input DEM files are NLS 10m DEM already available in **Puhti&#39;s GIS data folder** : `/appl/data/geo/mml/dem10m/etrs-tm35fin-n2000/` If you want to preview the files with [QGIS](https://docs.csc.fi/apps/qgis/), open one or a few DEM files from [mapsheets.txt](mapsheets.txt) file. For seeing all Finland you can open `/appl/data/geo/mml/dem10m/vrt/etrs-tm35fin-n2000/whole\finland\hierarchical.vrt`.
* In each of the subfolders are files for one job type or parallel library. Each subfolder has 2 files:
    * An .R file for defining the tasks to be done.
    * A batch job .sh file for submitting the job to Puhti SLURM.

## Interactive working 

* Start an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/)
```
sinteractive -i
```
* Load R module and open R commandline. Optionally start [RStudio](https://docs.csc.fi/apps/r-env-singularity/#interactive-use-on-a-compute-node), 

```
module load r-env-singularity
start-r
```
* Check that needed R libraries are available in Puhti. Which libraries are used in this script? Check whether those libraries are available in RStudio, with (change to correct packages): 
```
require(rgdal)
```
* [01_serial/Contours_simple.R](01_serial/Contours_simple.R) file. This is normal R script, which uses a for loop for going through all 3 files. Copy-paste commands to R console (or run them from RStudio). 

* Check that there are new files in your work directory, check with `ls –l` or click the refresh button in WinSCP:
  - 3 countour shapefiles in `shape` folder.
* Optional, check your results with **QGIS**

## Simple batch job
For simple 1 core job, use the same R-script as for interactive working.

* [01_serial/serial_batch_job.sh](01_serial/serial_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which module is used?

* Submit batch job 
```
sbatch serial_batch_job.sh
``` 

* `sbatch` gives a job id, use it to check state and efficiency of our batch job with 
```
seff <jobid>
```

* Once the job is finished, see output in out.txt and any possible errors in err.txt. 
* Check that you have new files in the `shape` folder.
* Check the resources used in another way. Did you reserve a good amount of memory? 
```
sacct -j <jobid> -o elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in job.
	- AllocCPUS – how many CPUs were used

## Array job
[Array jobs](https://docs.csc.fi/computing/running/array-jobs/) are an easy way of taking advantage of Puhti's parallel processing capabilities. Array jobs are useful when same code is executed many times for different datasets or with different parameters. In GIS context a typical use would be to run some model on study area split into multiple files where output from one file doesn't have an impact on result of an other area. In real use, one the array job should last longer than in this example, at least 10-20 min, because there is always also overhead in starting new jobs.

In the array job example the idea is that the R script will run one process for every given input file as opposed to running a for loop within the script. That means that he R script has to read the given argument in. 

* [02_array/array_batch_job.sh](02_array/array_batch_job.sh) array job batch file. Changes compared to simple serial job:
    * `--array` parameter is used to tell how many jobs to start. Value 1-3 in this case means that `$SULRM_ARRAY_TASK_ID` variable will be from 1 to 3, which means we will use sed to read first three lines from our mapsheets.txt file and start three jobs for those files. 
	* Output from each job is written to `array_job_out_<array_job_id>.txt` and `array_job_err_<array_job_id>.txt` files. 
	* Memory and time allocations are per job.
	* The mapsheet name is provided as an argument in the batch job script to the R script. 
	
* [02_array/Contours_array.R](02_array/Contours_array.R). 
    * R script reads the input DEM file from a parameter, which is set inside the batch job file. 
	* For looped has been removed, because now each job calculates one file.
	
* Submit the array job
```
sbatch array_job.sh
```
* Check with seff and sacct how much time and resources you used?

## Parallel jobs 
In this case the R code takes care of dividing the work to 3 processes, one for each input file.  R has several packages for code parallelization, here examples for `snow`, `parallel` and `future` are provided. `future` package is likely easiest to use. `future` has also two internal optins `multicore` and `cluster`. `future` with `multicore` can be used in one node, so max 40 cores. `future` with `cluster` can be used on several nodes. 

* [05_parallel_future/parallel_batch_job_future_cluster.sh](05_parallel_future/parallel_batch_job_future_cluster.sh) batch job file for `future` with `multicore`.
	* `--ntasks=4` reserves 4 cores: `snow` and `future` with `cluster` option require one additional process for master process, so that if there are 3 mapsheets to process 4 cores have to be reserved
	* `--mem-per-cpu=1000` reserves memory per core
	* `srun singularity_wrapper exec RMPISNOW --no-save --slave -f Calc_contours_future_cluster.R` starts RMPISNOW which enables using several nodes. RMPISNOW can not be tested from Rstudio.
*  [05_parallel_future/Calc_contours_future_cluster.R](05_parallel_future/Calc_contours_future_cluster.R)
	* Note how cluster is started, processes divided to workers (`future-map()`) and cluster is stopped.
	* For looped has been removed, because now each job calculates one file.
	* Optional compare to [03_parallel_snow/Calc_contours_snow.R](03_parallel_snow/Calc_contours_snow.R). `future` package takes care of exporting variables and libraries to workers itself, in `snow` and `parallel` it is user's responsibility.

* Submit the parallel job to Puhti
```
sbatch parallel_batch_job_future_cluster.sh
```
* Check with seff and sacct how much time and resources you used?