# Python Puhti examples, calculate NDVI

Here are examples for running Python code on CSC's Puhti supercomputer as four different job styles: interactive, serial, array and embarrasingly/delightfully/naturally parellel. For parallel jobs there are 3 options with different Python libraries: `multiprocessing`, `joblib` and `dask`.  We'll take a look at these three and `GNUParallel`. The interactive style is best for developing your scripts, usually with limited test data. For computationally more demanding analysis you have to use Puhti's batch system for requesting the resources and running your scripts. 

## Example case

The example calculates NDVI (Normalized Difference Vegetation Index) from the Sentinel2 satellite image's red and near infrared bands. The reading, writing and calculation of NDVI are identical in all examples (with the exception of the Dask example) and only the method of parallelization changes (the code in the main function). 

Basic idea behind the script is to:

- Find red and near infrared channels of Sentinel L2A products from its `SAFE` folder and open the `jp2` files. -> `readImage`
- Read the data as `numpy` array with `rasterio`, scale the values to reflectance values and calculate NDVI index. -> `calculateNDVI`
- Save output as GeoTiff with `rasterio`. -> `saveImage`

Files in this example:

* The input **ESA Sentinel L2A images** are in JPG2000 format and are already stored in Puhti: `/appl/data/geo/sentinel/s2_example_data/L2A`. Puhti has only these example images, more [Sentinel L2A images are available from CSC Allas](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-allas).
* The example scripts are in subfolders by job type and used parallel library. Each subfolder has 2 files:
    * A **.py** file for defining the tasks to be done.
    * A batch job **.sh** file for submitting the job to Puhti batch job scheduler (SLURM).

## Let's get started 


If you haven't yet, get the example scripts to Puhti:

> [!WARNING]
> Please note that you will need to adapt the paths mentioned in this material. In most cases it is `cscusername` and `project_200xxxx` that need to be replaced with your CSC username and your projectname.

* Log in to Puhti web interface: https://puhti.csc.fi
* Start a `Login node shell`
* Create a folder for yourself:
    * Switch to your projects scratch directory and further int the students directory: `cd /scratch/project_200xxxx/students` (fill in your project number for x)
    * Create new own folder:`mkdir cscusername` (replace cscusername with your username)
    * Switch into your own folder: `cd cscusername` (replace cscusername with your username)
    * Get the exercise material by cloning this repository: `git clone https://github.com/csc-training/geocomputing`
    * Switch to the directory with example files: `cd python/puhti`.
    * Check that we are in the correct place: `pwd` should show something like `/scratch/project_200xxxx/students/cscusername/python/puhti`.
    
    
## Interactive job

Within an [interactive job](https://docs.csc.fi/computing/running/interactive-usage/) it is possible to edit the script in between test-runs; so this suits best when still writing the script. Usually it is best to use some smaller test dataset for this.

### Jupyter

If you want to start prototyping and testing in a Jupyter Notebook, you can start with an interactive Jupyter session. Choose **Jupyter** from the Puhti web interface dashboard or the Apps tab in the Puhti web interface. We can find one such prototype file for calculating the NDVI for one file in the materials called `interactive.py`. It introduces the packages and workflow for this lesson. I

* Settings for Jupyter:
    * Project: project_200xxxx
    * Partition: interactive
    * Number of CPU cores: 1
    * Memory: 4 Gb
    * Local disk: 0
    * Time: 2:00:00
    * Python: geoconda
    * `Launch`

* Wait a moment -> Connect to Jupyter
* Jupyter opens up in the browser
* Open folder with the exercise files from the left browser panel `/scratch/project_200xxxx/cscusername/geocomputing/python/puhti` and find the file `interactive.ipynb`. Execute each code cell one after the other with `Shift+Enter`.

As mentioned, Jupyter is nice for prototyping and testing, however if we want to use this process as part of a larger script, or make it possible to more easily adapt the script to run on other files or calculate other vegetation indices, we need to generalize it and put the code in a Python script. This means for example to put parts into functions, so that they can be reused. You can find one such cleaned up and generalized script with much more comments in `00_interactive/interactive_single_core_example.py`. 

> [!NOTE]
> Take a look at how it differs and think about what we can do with it.

### Interactive job with Python script

#### Visual Studio Code

Visual Studio Code or VSCode is a source code editor by Microsoft. In addition to being able to run the full script within Visual Studio Code, it also possible to run parts of a script step by step.

* Start [Visual Studio Code](https://docs.csc.fi/computing/webinterface/vscode/) in [Puhti web interface](https://docs.csc.fi/computing/webinterface/).
    * Open VSCode start page from front page: Apps -> Visual Studio code
    * Choose settings for VSCode:
        * Project: project_200xxxx
        * Partition: interactive
        * Number of CPU cores: 1
        * Memory: 4 Gb
        * Local disk: 0
        * Time: 1:00:00
        * Modules: geoconda
        * `Launch`
    * Wait a moment -> Connect to Visual studio code
    * VSCode opens up in the browser
* Open folder with exercise files: 
    * File -> Open folder -> `/scratch/project_200xxxx/students/cscusername/geocomputing/python/puhti`` -> OK
* Open [00_interactive/interactive_single_core_example.py](01_serial/single_core_example.py). This is a Python script, which calculates NDVI for one input Sentinel-2 "file". 
* Check that needed Python libraries are available in Puhti:
    * Select all import rows and press `Shift+Enter`. Wait a few seconds. The import commands are run in Terminal (which opens automatically on the bottom of the page). If no error messages are visible, the packages are available. Also other parts of the script can be tested in the same manner (select the code and run with `Shift+Enter`).
* We can also run the full script by following these steps: 
    * Exit Python console in Terminal: type `exit()` in the terminal, if you ran pieces of the code before.
    * Click green arrow above script (Run Python File in Terminal)
    * Wait, it takes a few minutes for complete. The printouts will appear  in the terminal during the process.
    * Check that there is one new GeoTiff file in your work directory in the Files panel of VSCode.
* Optional, check your results with [QGIS](https://docs.csc.fi/apps/qgis/)

#### Command line

If you prefer working in the command line, you can also start an interactive job in the webinterface, by starting a compute node shell directly from the tools tab in Puhti web interface. Choose settings for the interactive session:

* Project: project_200xxxx
* Number of CPU cores: 1
* Memory: 4 Gb
* Local disk: 0
* Time: 1:00:00

> [!NOTE]
> You can also start an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/) from a login node (by starting a login node shell from tools tab in Puhti webinterface or by connecting to Puhti via ssh in your own computers terminal) with:

>  `sinteractive --account project_200xxxx --cores 1 --time 02:00:00 --mem 4G --tmp 0` 

> This gives you a compute node shell; you can see "where" you are from your terminal prompt [cscusername@puhti-loginXX] -> login node, [cscusername@rXXcXX] (XX being some numbers) -> compute node. 

For both of the above:

After getting access to the compute node shell, you can load modules and run scripts "like on a normal linux computer":

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
module load geoconda
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/01_serial
python single_core_example.py /appl/data/geo/sentinel/s2_example_data/L2A
```

* Wait, it takes a few minutes for complete. The printouts will appear  in the terminal during the process.
* Check that there is one new GeoTiff file in your work directory in the Files panel of VSCode.
* Optional, check your results with [QGIS](https://docs.csc.fi/apps/qgis/)

## Serial job

What if we don't want the execution of the script blocking our command line? We need to start writing batch job scripts and separate the submission of the job on the login node from the execution of the job on a compute node -> We go non-interactive. **Latest now, we have to move to the terminal.**

* Open [01_serial/single_core_example.sh](01_serial/single_core_example.sh) with your favorite editor (e.g. `nano` in login node shell, open the editor via the three dots next to the filename in the webinterface>Files section or VSCode).

> [!NOTE]
> Can you find out from the `.sh` file: 
> * Where are output and error messages written?
> * How many cores are reserved, and for how long a time? 
> * How much memory?
> * Which partition is used?
> * Which module is used?
> * Does this all sound familiar? Yes, we have given these parameters before, just in a different way.

* Submit the batch job from **login node shell** (not VSCode terminal or compute node shell):

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/01_serial
sbatch single_core_example.sh
```

->  `sbatch` prints out a job ID

> [!NOTE]
> Use the job ID to check state and efficiency of the batch job with `seff jobid` (replace jobid with the job ID from the print out)
> Did you reserve a good amount of memory?


* Once the job is finished, see output in `slurm-jobid.out` and `slurm-jobid.err` (e.g. with `cat slurm-jobid.out`) for any possible errors and other outputs. 
* Check that you have a new GeoTiff file in the working folder.

You can also check the resources used for the job in another way:

```
sacct -j jobid -o JobName,elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

- elapsed – time used by the job
- TotalCPU – time used by all cores together
- reqmem – amount of requested memory
- maxrss – maximum resident set size of all tasks in job.
- AllocCPUS – how many CPUs were reserved


> [!NOTE]
> What if we want to run the same process for not only one, but all Sentinel-2 files within a folder? We could run the same script with different input one after another from the sbatch file, or adjust the Python script to take in the data folder instead of just one Sentinel-2 "file" and loop through all files in the main function (see `01_serial/single_core_example_folder.sh` and `01_serial/single_core_example_folder.py`). 


## GNU parallel

GNU parallel can help parallelizing a script which otherwise is not parallelized. In this example we want to run the same script on three different inputfiles which we can read into a textfile and use as argument for the parallel tool.

[02_gnu_parallel/gnu_parallel_example.sh](02_gnu_parallel/gnu_parallel_example.sh).
The only difference to serial job is that we do not loop through the directory inside the Python script but let GNU parallel handle that step.

> To get to know how many `cpus-per-task` we need you can use for example `ls /appl/data/geo/sentinel/s2_example_data/L2A | wc -l` to count everything within the data directory before writing the batch job script. 

Submit the job to Puhti from login node shell:

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/02_gnu_parallel
sbatch gnu_parallel_example.sh
```
> [!NOTE]
> Check with `seff`: How much time and resources did you use?

### Array job

In the array job example the idea is that the Python script will run one process for every given input file as opposed to running a for loop within the script or one job on multiple CPUs (GNU parallel). 

* [03_array/array_job_example.sh](03_array/array_job_example.sh) array job batch file. Changes compared to simple serial job:
    * `--array` parameter is used to tell how many jobs to start. Value 1-3 in this case means that `$SLURM_ARRAY_TASK_ID` variable will be from 1 to 3. We can use `sed` to read the first three lines from our `image_path_list.txt` file and start a job for each input file. 
	* Output from each job is written to `slurm-jobid_arrayid.out` and `slurm-jobid_arrayid.err` files. 
	* Memory and time allocations are per job.
	* The image name is provided as an argument in the batch job script to the Python script. 
	
* [03_array/array_job_example.py](03_array/array_job_example.py). 
    * Python script reads the input image file from the argument, which is set inside the batch job file. 
	* For loop has been removed, each job calculates only one file.
	
> [!NOTE]
> Submit the array job to Puhti from login node shell

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/03_array
sbatch array_job_example.sh
```

> [!NOTE]
> Check with `seff`: How much time and resources did you use?


## Parallelization within Python

We can also paralellize within Python. In this case there is no for loop to process them one after another, but the Python code takes care of dividing the work to 3 processes running at the same time, one for each input file. Python has several packages for code parallelization, here examples for `multiprocessing`, `joblib` and `dask` are provided. `multiprocessing` package is likely easiest to use and is included in all Python installations by default. `joblib` provides some more flexibility. `multiprocessing` and `joblib` are suitable for one node (max 40 cores). 

### Multiprocessing

* [04_parallel_multiprocessing/multiprocessing_example.sh](04_parallel_multiprocessing/multiprocessing_example.sh) batch job file for `multiprocessing`.
	* `--ntasks=1` + `--cpus-per-task=3` reserves 3 cores - one for each file
	* `--mem-per-cpu=4G` reserves memory per core

* [04_parallel_multiprocessing/multiprocessing_example.py](04_parallel_multiprocessing/multiprocessing_example.py)
	* Note how the pool of workers is started and processes divided to workers with `pool.map()`. This replaces the for loop in simple serial job.

> [!NOTE]
> Submit the parallel job to Puhti from login node shell

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/04_parallel_multiprocessing
sbatch multiprocessing_example.sh
```

> [!NOTE]
> Check with `seff`: How much time and resources did you use?

### dask

`dask` is versatile and has several options for parallelization, this example is for single-node (max 40 cores)- usage, but `dask` can also be used for multi-node jobs. This example uses [delayed functions](https://docs.dask.org/en/latest/delayed.html) from Dask to parallelize the workload. Typically, if a workflow contains a for-loop, it can benefit from delayed. [Dask delayed tutorial](https://tutorial.dask.org/03_dask.delayed.html)

* [06_parallel_dask/single_node/dask_singlenode.sh](06_parallel_dask/single_node/dask_singlenode.sh) batch job file for `dask`.
	* `--ntasks=1` + `--cpus-per-task=3` reserves 3 cores - one for each file
	* `--mem-per-cpu=4G` reserves memory per core

* [06_parallel_dask/single_node/dask_singlenode.py](06_parallel_dask/single_node/dask_singlenode.py)


> [!NOTE]
> Submit the parallel job to Puhti from login node shell

>[!NOTE]
> Remember to change the project name and your CSC user name in the paths below.

```
cd /scratch/project_200xxxx/cscusername/geocomputing/python/puhti/parallel_dask
sbatch dask_singlenode.sh
```

> [!NOTE]
> Check with `seff`: How much time and resources did you use?

Another example using xarray in addition to dask is provided in [06_parallel_dask/single_node/dask_singlenode_xr.sh](06_parallel_dask/single_node/dask_singlenode_xr.sh).

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
