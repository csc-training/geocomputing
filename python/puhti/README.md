# Python Puhti examples, calculate NDVI

Here are examples for running Python code on CSC's Puhti supercluster as four different job styles: interactive, simple serial, array and parellel. For parallel jobs there are 3 options with different Python libraries: `multiprocessing`, `joblib` and `dask`. The interactive style is best for developing your scripts, usually with limited test data. For computationally more demanding analysis you have to use Puhti's batch system for requesting the resources and running your scripts. 

The example calculate NDVI (Normalized Difference Vegetation Index) from the Sentinel2 satellite image's red and near infrared bands. The reading, writing and calculation of NDVI are identical in all examples (with the exception of the Dask example) and only the method of parallelisation changes (the code in the main function). 

Basic idea behind the script is to:

- Find red and infrared channels of Sentinel 2A images from SAFE folder and open the files.
- Read the data as `numpy` array with `rasterio`, scale the values back to real reflectance values and calculate NDVI index.
- Save output as GeoTiff with `rasterio`.

If a Python script is ready on laptop, then for running it in Puhti normally you need to edit only the paths to files and folders. Sometimes it might be necessary to install [new Python libraries](https://docs.csc.fi/apps/geoconda/#adding-more-python-packages-to-geoconda).

Additional info: [Puhti batch job system documentation](https://docs.csc.fi/computing/running/creating-job-scripts/)

Files in this example:

* The input **ESA Sentinel L2A images** are in JPG2000 format and are already stored in Puhti: `/appl/data/geo/sentinel/s2_example_data/L2A`. Puhti has only these example images, more [Sentinel L2A images are available from CSC Allas](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-allas).
* The example scripts are in subfolders by job type and used parallel library. Each subfolder has 2 files:
    * A **.py** file for defining the tasks to be done.
    * A batch job **.sh** file for submitting the job to Puhti SLURM.

## Setting up - copying files to Puhti
* Log in to Puhti web interface: https://puhti.csc.fi
* Create a folder for yourself. 
    * From front page: Files -> /scratch/project_2000745/
	* Move to students folder: click the folder name
    * Create new own folder: New Directory ->  [your_username] -> OK
	* Open your own folder: click the name of your folder
* Download exercise files from Github to Puhti 
    * Open SSH terminal in side your own folder: Open in Terminal
    * Clone this repository: `git clone https://github.com/csc-training/geocomputing`
	
## Interactive job

Start [VSCode](https://docs.csc.fi/computing/webinterface/vscode/) in an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/) with [Puhti web interface](https://docs.csc.fi/computing/webinterface/).

* Open VSCode start page from front page: `Apps -> Visual Studio code`
* Choose settings for VSCode:
    * Project: project_2000745
    * Particion: interactive
    * Number of CPU cores: 1
    * Memory: 4 Gb
    * Local disk: 0
    * Time: 2:00:00
    * Modules: geoconda
    * `Launch`
* Wait a moment -> Connect to Visual studio code
* VSCode opens up in the browser
* Open folder with exercise files: File -> Open folder -> /scratch/project_2000745/students/[your_username]/geocomputing/python/puhti -> OK

* Open [01_serial/single_core_example.py](01_serial/single_core_example.py). This is basic Python script, which uses a **for loop** for going through all 3 files.  
* Check that needed Python libraries are available in Puhti. Which libraries are used in this script? Check whether those libraries are available. Select all import rows and press `Shift+Enter`. The import commands are run in Terminal. If no error messages are visible, the packages are available.
* Optional, for more advanced option for running Python code in VSCode, see for example [VSCode's Python Interactive mode is AMAZING!](https://www.youtube.com/watch?v=lwN4-W1WR84) and [How to Debug Python with VSCode](https://www.youtube.com/watch?v=w8QHoVam1-I&t=19s) videos.
* Run the full script: 
    * Exit Python console in Terminal: `exit()`
	* Click green arrow above script (Run Python File in Terminal)
    * Wait, it takes a few minutes for complete. The printouts will appear during the process.
    * Check that there are 3 new GeoTiff files in your work directory in the Files pane of VSCode.
* Optional, check your results with [QGIS](https://docs.csc.fi/apps/qgis/)


## Serial job
For simple 1 core batch job, use the same Python-script as for interactive working.

* Open [01_serial/single_core_example.sh](01_serial/serial_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which module is used?
* Submit batch job from SSH terminal
```
cd /scratch/project_2000745/students/[your_username]/geocomputing/python/puhti/01_serial
sbatch single_core_example.sh
``` 
* `sbatch` prints out a job ID, use it to check state and efficiency of the batch job. Did you reserve a good amount of memory?
```
seff [jobid]
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. 
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
sbatch array_job_example.py
```
* Check with `seff` and `sacct` how much time and resources you used?


## Example benchmarks 

These are just to demonstrate the difference between single core vs. some kind of parallelism. Depending on the issue, some library might be faster or slower.

| Example         | Jobs | CPU cores / job | Time (min) | CPU efficiency |
|-----------------|------|-----------------|------------|----------------|
| single core     | 1    | 1               | 03:23      | 86.70%         |
| multiprocessing | 1    | 3               | 01:05      | 92.31%         |
| joblib          | 1    | 3               | 01:12      | 86.57%         |
| dask            | 1    | 3               | 01:22      | 78.46%         |
| array job       | 3    | 1               | 01:03      | 95.16%         |
