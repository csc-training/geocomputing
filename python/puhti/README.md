# Python Puhti examples, calculate NDVI

Here are examples for running Python code on CSC's Puhti supercluster as four different job styles: interactive, serial, array and embarrasingly/delightfully/naturally parellel. For parallel jobs there are 3 options with different Python libraries: `multiprocessing`, `joblib` and `dask`.  We'll take a look at `multiprocessing`,`dask` and `GNUParallel`. The interactive style is best for developing your scripts, usually with limited test data. For computationally more demanding analysis you have to use Puhti's batch system for requesting the resources and running your scripts. 

## Example case

The example calculate NDVI (Normalized Difference Vegetation Index) from the Sentinel2 satellite image's red and near infrared bands. The reading, writing and calculation of NDVI are identical in all examples (with the exception of the Dask example) and only the method of parallelisation changes (the code in the main function). 

Basic idea behind the script is to:

- Find red and near infrared channels of Sentinel L2A products from its `SAFE` folder and open the `jp2` files. -> `readImage`
- Read the data as `numpy` array with `rasterio`, scale the values to reflectance values and calculate NDVI index. -> `calculateNDVI`
- Save output as GeoTiff with `rasterio`. -> `saveImage`

> [!NOTE]
> A Python script that was written and run on your own computer and that does not have any hard-coded file dependecies, can also be run on Puhti. If you call any absolute filepaths (= hard-coded dependency, auch as `/my/home/dir/file.txt`; not recommended!) within your script, you need to update these paths and copy the files to Puhti. Also check that all used Python packages are available on Puhti, eg within the [geoconda module](https://docs.csc.fi/apps/geoconda). If needed, you can [add Python packages for your own usage](https://docs.csc.fi/apps/python/#installing-python-packages-to-existing-modules) also yourself.
> Also read the [Puhti batch job system documentation](https://docs.csc.fi/computing/running/getting-started/)



Files in this example:

* The input **ESA Sentinel L2A images** are in JPG2000 format and are already stored in Puhti: `/appl/data/geo/sentinel/s2_example_data/L2A`. Puhti has only these example images, more [Sentinel L2A images are available from CSC Allas](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-allas).
* The example scripts are in subfolders by job type and used parallel library. Each subfolder has 2 files:
    * A **.py** file for defining the tasks to be done.
    * A batch job **.sh** file for submitting the job to Puhti batch job scheduler (SLURM).

## Let's get started 
### Get example scripts to Puhti

* Log in to Puhti web interface: https://puhti.csc.fi
* Start a `Login node shell`
* Create a folder for yourself:
    * Switch to your projects scratch directory: `cd /scratch/project_200xxxx/` (fill in your project number for x)
    * Create new own folder:`mkdir <your_username>` (fill in your user name for y)
    * Switch into your own folder: `cd <your_username>` (fill in your username for y)
    * Get the exercise material by cloning this repository: `git clone https://github.com/csc-training/geocomputing`
    * Switch to the directory with example files: `cd python/puhti`.
    * Check that we are in the correct place: `pwd` should show something like `/scratch/project_200xxxx/<your_username>/python/puhti`.
    
    
## Interactive job

Within an [interactive job](https://docs.csc.fi/computing/running/interactive-usage/) it is possible to edit the script in between test-runs; so this suits best when still writing the script. Usually it is best to use some smaller test dataset for this.

### Visual Studio Code

With Visual Studio Code you can also just run parts of the script.

* Start [Visual Studio Code](https://docs.csc.fi/computing/webinterface/vscode/) in [Puhti web interface](https://docs.csc.fi/computing/webinterface/).
    * Open VSCode start page from front page: Apps -> Visual Studio code
    * Choose settings for VSCode:
        * Project: project_200xxxx
        * Partition: interactive
        * Number of CPU cores: 1
        * Memory: 4 Gb
        * Local disk: 0
        * Time: 2:00:00
        * Modules: geoconda
        * `Launch`
    * Wait a moment -> Connect to Visual studio code
    * VSCode opens up in the browser
* Open folder with exercise files: 
    * File -> Open folder -> /scratch/project_200xxxx/<your_username>/geocomputing/python/puhti -> OK
* Open [01_serial/single_core_example.py](01_serial/single_core_example.py). This is a Python script, which uses a **for loop** for going through all 3 files.  
* Check that needed Python libraries are available in Puhti. If it is not your own script you can see which libraries are used in this script by checking the imports. To check whether those libraries are available: Select all import rows and press `Shift+Enter`. Wait a few seconds. The import commands are run in Terminal (which opens automatically on the bottom of the page). If no error messages are visible, the packages are available. Also other parts of the script can be tested in the same manner (select the code and run with `Shift+Enter`).
* Run the full script: 
    * Exit Python console in Terminal: type `exit()` in the terminal
    * Click green arrow above script (Run Python File in Terminal)
    * Wait, it takes a few minutes for complete. The printouts will appear during the process.
    * Check that there are 3 new GeoTiff files in your work directory in the Files panel of VSCode.
* Optional, check your results with [QGIS](https://docs.csc.fi/apps/qgis/)



## Serial job
For simple 1 core batch job, use the same Python-script as for interactive working.

* Open [01_serial/single_core_example.sh](01_serial/serial_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which module is used?
* Submit batch job from SSH terminal (in Puhti web interface the login node shell, not VSCode Terminal)
```
cd /scratch/project_2000745/[your_username]/geocomputing/python/puhti/01_serial
sbatch single_core_example.sh
``` 
* `sbatch` prints out a job ID, use it to check state and efficiency of the batch job. Did you reserve a good amount of memory?
```
seff [jobid]
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. Open the files with VSCode. 
* Check that you have new GeoTiff files in working folder.
* Check the resources used in another way. 
```
sacct -j [jobid] -o JobName,elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in job.
	- AllocCPUS – how many CPUs were reserved


## Parallel job
In this case the Python code takes care of dividing the work to 3 processes, one for each input file. Python has several packages for code parallelization, here examples for `multiprocessing`, `joblib` and `dask` are provided. `multiprocessing` package is likely easiest to use and in inlcuded in all Python installations by default. `joblib` provides some more flexibility. `multiprocessing` and `joblib` are suitable for one node (max 40 cores). `dask` is the most versatile has several optins for parallelization, the examples here include both single-node (max 40 cores) and multi-node example.

* [03_parallel_multiprocessing/multiprocessing_example.sh](03_parallel_multiprocessing/multiprocessing_example.sh) batch job file for `multiprocessing`.
	* `--ntasks=1` + `--cpus-per-task=3` reserves 3 cores - one for each file
	* `--mem-per-cpu=4G` reserves memory per core

* [03_parallel_multiprocessing/multiprocessing_example.py](03_parallel_multiprocessing/multiprocessing_example.py)
	* Note how pool of workers is started and processes divided to workers with `pool.map()`. This replaces the for loop in simple serial job.

* Submit the parallel job to Puhti from SSH terminal
```
cd ../03_parallel_multiprocessing
sbatch multiprocessing_example.sh
```
* Check with `seff` and `sacct` how much time and resources you used?

## Array job
[Array jobs](https://docs.csc.fi/computing/running/array-jobs/) are an easy way of taking advantage of Puhti's parallel processing capabilities. Array jobs are useful when same code is executed many times for different datasets or with different parameters. In GIS context a typical use case would be to run some model on study area split into multiple files where output from one file doesn't have an impact on result of an other area. 

In the array job example the idea is that the Python script will run one process for every given input file as opposed to running a for loop within the script. That means that the Python script has to read the file to be processed from commandline  argument. 

* [02_array/array_job_example.sh](02_array/array_job_example.sh) array job batch file. Changes compared to simple serial job:
    * `--array` parameter is used to tell how many jobs to start. Value 1-3 in this case means that `$SULRM_ARRAY_TASK_ID` variable will be from 1 to 3. With `sed` read first three lines from our `image_path_list.txt` file and start a job for each input file. 
	* Output from each job is written to `array_job_out_<array_job_id>.txt` and `array_job_err_<array_job_id>.txt` files. 
	* Memory and time allocations are per job.
	* The image name is provided as an argument in the batch job script to the Python script. 
	
* [02_array/array_job_example.py](02_array/array_job_example.py). 
    * Python script reads the input image file from the argument, which is set inside the batch job file. 
	* For looped has been removed, each job calculates only one file.
	
* Submit the array job
```
cd ../02_array
sbatch array_job_example.sh
```
* Check with `seff` and `sacct` how much time and resources you used?

## GNU parallel

GNU parallel can help parallelizing a script which otherwise is not parallelized. In this example we want to run the same script on three different inputfiles which we can read into a textfile and use as argument to the parallel tool.

This is similar to array jobs (see [Geocomputing array job example](https://github.com/csc-training/geocomputing/tree/master/python/puhti/02_array)), with the advantage that we do not start and need to monitor multiple jobs.

[gnu_parallel/gnu_parallel_example.sh](gnu_parallel/gnu_parallel_example.sh).
The only difference to serial job is that we do not loop through the directory inside the Python script but let GNU parallel handle that step.

> To get to know how many `cpus-per-task` we need you can use for example `ls /appl/data/geo/sentinel/s2_example_data/L2A | wc -l` to count everything within the data directory before writing the batch job script. 

Submit the gnu_parallel job
```
cd ../gnu_parallel
sbatch gnu_parallel_example.sh
```
* Check with `seff` how much time and resources you used?

## Example benchmarks 

These are just to demonstrate the difference between single core vs. some kind of parallelism. Depending on the issue, some library might be faster or slower.

| Example         | Jobs | CPU cores / job | Time (min) | CPU efficiency |
|-----------------|------|-----------------|------------|----------------|
| single core     | 1    | 1               | 03:23      | 86.70%         |
| multiprocessing | 1    | 3               | 01:05      | 92.31%         |
| joblib          | 1    | 3               | 01:12      | 86.57%         |
| dask            | 1    | 3               | 01:22      | 78.46%         |
| array job       | 3    | 1               | 01:03      | 95.16%         |
| GNU parallel    | 1    | 3               | 00:55      | 15.15%         |