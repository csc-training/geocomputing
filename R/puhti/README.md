# R Puhti examples, calculating contours
Here are examples for running R code on CSC's Puhti supercluster as four different job styles: interactive, simple serial, array and parellel. For parallel there are 3 options with different R libraries: `snow`, `parallel` and `future`. The interactive style is best for developing your scripts, usually with limited test data. For computationally more demanding analysis you have to use Puhti's batch system for requesting the resources and running your script. 

The contours are calculated based on NLS 10m DEM data in geotiff format with `raster` package. The results are saved in GeoPackge format. 

If an R script is ready on laptop, then for running it in Puhti normally you need to edit only the paths to files and folders. Sometimes it might be necessary to install [new R libraries](https://docs.csc.fi/apps/r-env-singularity/#r-package-installations).

Additional info: [Puhti batch job system documentation](https://docs.csc.fi/computing/running/creating-job-scripts/)

Files in this example:
* [mapsheets.txt](mapsheets.txt) file - list of mapsheets to process. Open the file. How many mapsheets (=files) there is?
* The input NLS 10m DEM is already available in **Puhti&#39;s GIS data folder** : `/appl/data/geo/mml/dem10m/2019/` If you want to preview the files with [QGIS](https://docs.csc.fi/apps/qgis/), open one or a few DEM files from [mapsheets.txt](mapsheets.txt) file. For seeing all Finland you can open `/appl/data/geo/mml/dem10m/dem10m_hierarchical.vrt`.
* In each of the subfolders here are files for one job type or parallel library. Each subfolder has 2 files:
    * An .R file for defining the tasks to be done.
    * A batch job .sh file for submitting the job to Puhti SLURM.

## Interactive working 

* Open [Puhti web interface](https://puhti.csc.fi) and log in with CSC user account.
* Start [interactive session](https://docs.csc.fi/computing/running/interactive-usage/) and start RStudio. `Apps -> RStudio`
  * Project: project_2002044
  * Partition: interactive
  * CPU cores: 1
  * Memory: 4
  * Local disk: 2
  * Time: 2:00:00
  * R version: [r-env-singularity/4.0.5](https://docs.csc.fi/apps/r-env-for-gis/)

* Get exercise materials. Clone [geocomputing Github](https://github.com/csc-training/geocomputing) repository. In RStudio: `File -> New project -> Version control -> Git`
  * Repository URL: https://github.com/csc-training/geocomputing.git
  * Project directory name: geocomputing
  * Create project as subdirectory of -> `Browse -> ... (in upper right corner) -> Path to folder`: /scratch/project_2002044/students/<your_account_name>  (if you do not yet have a directory there, use /scratch/project_2002044/students/ as path to folder and create a new directory with your account name and enter it)
* Move to folder `R/puhti/01_serial`.
* Set the working directory. `Session -> Set working directory -> To Files Pane location`

* Open [01_serial/Contours_simple.R](01_serial/Contours_simple.R). This is basic R script, which uses a **for loop** for going through all 3 files. 
* Check that needed R libraries are available in Puhti. Which libraries are used in this script? Run the libraries loading part in RStudio. 
* Run the rest of the commands from RStudio. 
* Check that there are 3 Geopackage files with contours in your work directory in RStudio.
* Optional, check your results with **[QGIS](https://docs.csc.fi/apps/qgis/)**

## Simple batch job
For simple 1 core batch job, use the same R-script as for interactive working.

* [01_serial/serial_batch_job.sh](01_serial/serial_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which module is used?

* Open another web tab with Puhti shell (`Tools -> Puhti shell access`) and submit batch job. (Use Shift-Insert or Ctrl+V for paste.)
```
cd /scratch/project_2002044/students/<your_account_name>/geocomputing/R/puhti/01_serial
sbatch serial_batch_job.sh
``` 
* `sbatch` prints out a job id, use it to check the state and the efficiency of the batch job. Did you reserve a good amount of memory?
```
seff <jobid>
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. 
* Check that you have 3 new GeoPackge files in the working folder.
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
In this case the R code takes care of dividing the work to parallel processes, one for each input file.  R has several packages for code parallelization, here examples for `snow`, `parallel` and `future` are provided. `future` package is likely easiest to use. `future` has also two internal optins `multicore` and `cluster`. `parallel` and `future` with `multicore` can be used in one node, so max 40 cores. `snow` and`future` with `cluster` can be used on several nodes. 

* [05_parallel_future/parallel_batch_job_future_cluster.sh](05_parallel_future/parallel_batch_job_future_cluster.sh) batch job file for `future` with `cluster`.
	* `--ntasks=4` reserves 4 cores: `snow` and `future` with `cluster` option require one additional process for master process, so that if there are 3 mapsheets to process 4 cores have to be reserved
	* `--mem-per-cpu=1000` reserves memory per core
	* `srun singularity_wrapper exec RMPISNOW --no-save --slave -f Calc_contours_future_cluster.R` starts `RMPISNOW` which enables using several nodes. `RMPISNOW` can not be tested from Rstudio.
*  [05_parallel_future/Calc_contours_future_cluster.R](05_parallel_future/Calc_contours_future_cluster.R)
	* Note how cluster is started, processes divided to workers with `future-map()` and cluster is stopped.
	* For looped has been removed, each worker calculates one file.
	* Optional, compare to [03_parallel_snow/Calc_contours_snow.R](03_parallel_snow/Calc_contours_snow.R). `future` package takes care of exporting variables and libraries to workers itself, in `snow` and `parallel` it is user's responsibility.

* Submit the parallel job to Puhti
```
sbatch parallel_batch_job_future_cluster.sh
```
* Check with `seff` and `sacct` how much time and resources you used?

## Array job
[Array jobs](https://docs.csc.fi/computing/running/array-jobs/) are an easy way of taking advantage of Puhti's parallel processing capabilities. Array jobs are useful when same code is executed many times for different datasets or with different parameters. In GIS context a typical use case would be to run some model on study area split into multiple files where output from one file doesn't have an impact on result of an other area. 

In the array job example the idea is that the R script will run one process for every given input file as opposed to running a for loop within the script. That means that the R script has to read the file to be processed from commandline  argument. 

* [02_array/array_batch_job.sh](02_array/array_batch_job.sh) array job batch file. Changes compared to simple serial job:
    * `--array` parameter is used to tell how many jobs to start. Value 1-3 in this case means that `$SULRM_ARRAY_TASK_ID` variable will be from 1 to 3. With `sed` read first three lines from `mapsheets.txt` file and start a job for each input file. 
	* Output from each job is written to `array_job_out_<array_job_id>.txt` and `array_job_err_<array_job_id>.txt` files. 
	* Memory and time allocations are per job.
	* The image name is provided as an argument in the batch job script to the R script. 
	
* [02_array/Contours_array.R](02_array/Contours_array.R). 
    * R script reads the input DEM file from the argument, which is set inside the batch job file. 
	* For looped has been removed, each job calculates only one file.
	
* Submit the array job
```
sbatch array_job.sh
```
* Check with `seff` and `sacct` how much time and resources you used?
