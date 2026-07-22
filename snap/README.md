# SNAP GPT examples for Roihu

This folder includes example files for [SNAP](https://earth.esa.int/eogateway/tools/snap) for Roihu supercomputer. Read the [CSC Docs: SNAP page](https://docs.csc.fi/apps/snap/) before continuing. 

The examples use [SNAP GPT](https://step.esa.int/main/wp-content/help/?version=13.0.0&helpid=gpf.graphProcessingTool), to run the computations from commandline.

The examples show how to run:

* One SNAP GPT Graph in **serial mode** with one set of inputs.
* The same Graph with 4 different inputs in **parallel** with `xargs`.

## Preparations
* Make a folder for the exercise materials and make it your working directory
* Change the project name and username.

```
mkdir -p /scratch/project_200XXXX/students/$USER
cd /scratch/project_200XXXX/students/$USER
```

* Copy the example scripts to Roihu.
```
git clone https://github.com/csc-training/geocomputing.git
```

* Move to the SNAP exercise folder.
```
cd geocomputing/snap
```

## The SNAP GPT process

The example GPT graph stacks 2 files to one. As example NLS 10m DEM and LUKE 10m erosion risk datasets are used, because these are already available in Roihu. Normally SNAP is used with Sentinel satellite data.

Common files for both examples:

* [snap_graph_stacking.xml](snap_graph_stacking.xml)-file - the SNAP Graph that defines the processing workflow. 
* [process_one_file.sh](process_one_file.sh) - bash script to run the SNAP Graph for one set of inputs. It also sets custom user dir for temporary files and memory settings.

Open both files and check the contents, but no changes are needed to these files.

## Serial job

We will use Roihu web interface simple file editor for editing the files in this exercise. 

* Open another tab in your web browser to [Roihu web interface](https://roihu.csc.fi).
* Open Files -> `/scratch/project_200XXXX`
* Open folders: `students` -> `cscusername` -> `geocomputing` -> `snap`

Open the files with Edit under the menu on the right of the file name. 
* [snap_serial_job.sh](snap_serial_job.sh) - the batch job script that makes resource (time, memory, cores) reservations to Roihu and starts the gpt command. The batch job file [is submitted to the Roihu queuing system](https://docs.csc.fi/computing/running/submitting-jobs/) the batch job script. How many cores and for how long time are they reserved? How much memory? Which partition is used? Which modules are used?
	* Change the project name in `#SBATCH --account` setting. Save.


* In the Login shell window, run the script as batch file: 
```
sbatch snap_serial_job.sh
```
* See output of slurm-<job_id>.out and slurm-<job_id>.err for any possible errors and other outputs.
	* For seeing the files use Roihu web interface or Linux `less <filename>`
 	* With `tail -f slurm-<job_id>.out` it is possible to see also how the output files are written during the job.
* Check that you have new GeoTiff file in the working folder. Check the result file with `gdalinfo`. 

* `sbatch` prints out a job id, use it to check the state and efficiency of the batch job. Did you reserve a good amount of memory? How long did the script run?
```
seff <job_id>
```
* Check the resources used in another way.
```
sacct -j <job_id> -o elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```

	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in the job.
	- AllocCPUS – how many CPUs were reserved


## Parallel job with `xargs`

`xargs` is used for handling several files in parallel. In this way, max one node (= 386 cores in Roihu) can be used. If even more is needed, see ["Workflow for many small, independent runs" tutorial](https://docs.csc.fi/support/tutorials/many/) how to combine this with array jobs. 

Open the files with Edit:
* [filelist.csv](filelist.csv) - list of files to process. In one row are inputs for 1 job: 2 input files separted with command and output file, separatad with `;`.
* [snap_xargs_parallel_job.sh](snap_xargs_parallel_job.sh) - the batch job script. How many cores are reserved? How much memory?  
	* Change the project name in `#SBATCH --account` setting. Save.
   
* Run the script as batch file: 
```
sbatch snap_array_job.sh
```
* Check the parallel batch job results with `seff`. Did you reserve a good amount of memory? What was the CPU-efficiency? How long did the script run?
* The script should create 4 .tif files to the working directory (one is overwritten from serial job).
