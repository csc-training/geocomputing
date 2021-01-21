## Overview
This is an example for running R code on CSC's Puhti supercluster as three different job styles: simple serial, array and parellel. In this example we'll calculate contours based on a geotiff image

The main tasks in this example:
* Creating needed folders
* Calculating the contours and saving them in Shape format.
* In all three scripts the same tasks are done to 3 mapsheets.

Contents of this example
* mapsheets.txt file, which defines which mapsheets will be processed. 
*	In each of the subfolders are files for one job type. There is 2 files:
**	An .R file for defining the tasks to be done.
** An .sh file for submitting the job to SLURM: `serial_batch_job.sh`, `array_job.sh` and `parallel_batch_job.sh`

A more detailed documentation on batch job system can be found here: https://docs.csc.fi/computing/running/creating-job-scripts/

## The serial R script
This is a basic R script, which uses a for loop for going through all 3 files.

## Simple batch job file

In the batch job file `serial_batch_job.sh` we define where the output and error messages are written as well as computing resources assigned for our program. In this case 5 minutes of execution time on once cpu and 1Gb of memory is plenty.

Batch job can then be submitted with command `sbatch serial_batch_job.sh`. This will also give us a job id which we can use to check state and efficiency of our batch job with `seff <jobid>`.

Once the job is finished we can see output in out.txt and any possible errors in err.txt

## Array jobs and R-spatial in Puhti
Array jobs are an easy way of taking advantage of Puhti's parallel processing capabilities. For more detailed instructions on array jobs see: https://docs.csc.fi/computing/running/array-jobs/

Array jobs are useful when same code is executed many times for different datasets or with different parameters. In GIS context a typical use would be to run some model on study area split into multiple files where output from one file doesn't have an impact on result of an other area. 

In the array job example we will provide the mapsheet as an argument in the batch job script. That means that he R script has to read the given argument in. Also the for looped has been removed, because now we are calculating one file per one job.

`--array` parameter is used to tell how many jobs we want to start. Value 1-3 in this case means we will have `$SULRM_ARRAY_TASK_ID` variable running from 1 to 3, which means we will use sed to read first three lines from our mapsheets.txt file and start three jobs for those files. If we want to process all files in the file list we should set `--array=1-<number of lines>`

Output from each job is written to `array_job_out_<array_job_id>.txt` and `array_job_err_<array_job_id>.txt` files. Memory and time allocations are per job, so we don't have to modify them from last example.

We can then submit this array job file with:
`sbatch array_job.sh`

## Using snow library for parallel processing
In this case the R code takes care of dividing the work to 3 processes, one for each input file. The snow package is used for multiprocessing.

## Using foreach with doMPI library for parallel processing
As above the R code takes care of dividing the work. Instead of snow, foreach and doMPI are used.

## Using future library for parallel processing
As above the R code takes care of dividing the work. Instead of snow, future package is used. Future package is likely easiest to use.
