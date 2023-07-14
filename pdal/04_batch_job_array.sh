#!/bin/bash -l
#Name of the job, this makes it easier to identify your job
#SBATCH -J batch_job_array
#SBATCH --account=project_2000599

#Outputfile. Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH --output output_%j.txt

#As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH --error error_%j.txt

#Partition you want to submit your job to. Possible values are serial, parallel, longrun, hugemem and test. In this excerecise we use test as it is for testing, but it shouldn't be used for serious work. See [Taito user guide](https://research.csc.fi/taito-constructing-a-batch-job-file) for details. 
#SBATCH -p small

#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:05:00

#Tells the batch job system that this is an array job that should be run 4 times. During each run the $SLURM_ARRAY_TASK_ID variable will get different value ranging from 1 to 4. This will be used to select different input files.
#SBATCH --array=1-4

#Tells the batch job system that this is not a parallel task and only one task should be used. Note that this is one task per job, but array job will actually launch 3 simultaneous jobs.
#SBATCH --ntasks=1

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load geoconda
#Change to the directory where you have the files

cd /scratch/project_2000599/geocomputing/pdal
#Read the file to be processed from a list of input files. This is done by getting the line corresponding to the $SLURM_ARRAY_TASK_ID from the input file list.
input=$(sed -n "$SLURM_ARRAY_TASK_ID"p 04_filelist.csv)

#Create output name from input by exchanging .laz to .tif.
name=$(echo "$input" | cut -f 1 -d '.')
output=data/$(echo "$name" | cut -f 2 -d '/').tif


#Run the pipeline as in previous exercise. Note that it is possible to override input and output files in your pipeline json from the commandline.
pdal pipeline --readers.las.filename=$input --writers.gdal.filename=$output 02_pipeline.json


