# GDAL, using commandline tools with bash scripts and batch jobs

GDAL reprents here a commandline tool that is used via Linux bash scripts. The example includes:

* Using GDAL tools interactively.
* Using GDAL tools via batch jobs:
	* A basic serial batch job, where several files are handled in a bash script for loop, one after the other. Only 1 core is used.
	* Parallel batch job, where different files are handled in parallel with GNU-parallel. Up to one node can be used, in Puhti that is up to 40 cores.

GDAL includes many other useful [commandline tools](https://gdal.org/programs/index.html), which usually are very efficient. In this example, we will reproject the coordinate system of multiple files in a folder and save the file in Cloud-optimized format. Linux bash script is used for starting the GDAL commands.

> [!IMPORTANT]  
> In these scripts `project_2015299` has been used as example project name. Change the project name to your own CSC project name.
> `cscusername` is example username, replace with your username.

## Preparations
* Make a folder for the exercise materials and make it your working directory
	* Change the project name and username.
```
mkdir -p /scratch/project_2015299/students/cscusername
cd /scratch/project_2015299/students/cscusername
```

* Copy the example scripts to Puhti.
```
git clone https://github.com/csc-training/geocomputing.git
```

* Move to the GDAL exercise folder.
```
cd geocomputing/gdal
``` 

## Interactive working 

With `gdalinfo` and `ogrinfo` it is often helpful to check the files. This is a light-weight task, so it can be done from the login node without an interactive session.

* Open [Puhti web interface](https://puhti.csc.fi) and log in with CSC user account.
* Open login node shell: `Tools -> Login node shell`
* To have GDAL tools available, load [geoconda module](https://docs.csc.fi/apps/geoconda/). Also several other modules include GDAL tools, see [CSC Docs: GDAL page](https://docs.csc.fi/apps/gdal/) for details.
```
module load geoconda
```
* Check a file with `gdalinfo`. What is the coordinate system? Is the file internally tiled? Does it have overviews?
```
gdalinfo /appl/data/geo/mml/dem10m/2019/W3/W33/W3333.tif
```

> [!IMPORTANT]  
> If you want to run more computationally heavy GDAL commands, then use [interactive session](https://docs.csc.fi/computing/running/interactive-usage/) on a compute node, easiest with a Compute node shell in the web interface.

## Serial batch job

We will use Puhti web interface simple file editor for editing the files in this exercise. 

* Open another tab in your web browser to [Puhti web interface](https://puhti.csc.fi).
* Open Files -> `/scratch/project_20xxxx`
* Open folders: `students` -> `cscusername` -> `geocomputing` -> `gdal`

Open the files with Edit under the menu on the right of the file name. 
* [gdal_serial.sh](gdal_serial.sh) - the bash script, includes GDAL commands to be executed. A for loop is used for handling several files.
	* Change the project name and username to yours in the GDAL command. Save.
* [gdal_batch_job_serial.sh](gdal_batch_job_serial.sh) - the batch job script. Where are the output and error messages written? How many cores and for how long time are they reserved? How much memory? Which partition is used? Which modules are used?
	* Change the project name in `#SBATCH --account` setting. Save.

* In the Login shell window, run the script as batch file: 
```
sbatch gdal_batch_job_serial.sh
```
* See output of slurm-<job_id>.out and slurm-<job_id>.err for any possible errors and other outputs.
	* For seeing the files use Puhti web interface or Linux `less <filename>`
 	* With `tail -f slurm-<job_id>.out` it is possible to see also how the output files are written during the job.
* Check that you have new GeoTiff files in the working folder. Check the result file with `gdalinfo`. What is the coordinate system? Are the files tiled? Do they have overviews?

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

> [!IMPORTANT]  
> Most GDAL tools support only usage of singe core, therefore in this example only 1 core is reserved and used. [gdalwarp](https://gdal.org/programs/gdalwarp.html) can benefit from multiple cores. If you are using `gdalwarp`, give the job more cores in the batch job file and add the [-multi](https://gdal.org/programs/gdalwarp.html#cmdoption-gdalwarp-multi) setting to the command in the bash script.

## Parallel job

GNU parallel is used for handling several files in parallel. In this way, max one node (= 40 cores in Puhti) can be used. If even more is needed, see ["Workflow for many small, independent runs" tutorial](https://docs.csc.fi/support/tutorials/many/) how to combine this with array jobs. 

Open the files with Edit:
* [gdal_parallel.sh](gdal_parallel.sh) - the bash script, it includes GDAL commands to be executed for one file. The for loop is removed.
	* No edits are needed, for only viewing the file, click the file name on the Files page.
* [gdal_batch_job_parallel.sh](gdal_batch_job_parallel.sh) - the batch job script. How many cores are reserved? How much memory? Which modules are used? 
	* Change the project name in `#SBATCH --account` setting. Save.
   
* Run the script as batch file: 
```
sbatch gdal_batch_job_parallel.sh
```
* Check the parallel batch job results with `seff`. Did you reserve a good amount of memory? What was the CPU-efficiency? How long did the script run?
