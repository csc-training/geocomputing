#!/bin/bash -l

#Name of the job, this makes it easier to identify your job
#SBATCH -J lidR_batch_job
#output_%j.txt - Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH -o batch_output_%j.txt
#error_%j.txt - As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH -e batch_error_%j.txt
#Partition you want to submit your job to. Possible values are serial, parallel, longrun, hugemem and test. In this excerecise we use test as it is for testing, but it shouldn't be used for serious work. See <link> for details.
#SBATCH -p test
#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#The number of cpus used by the lidR task
#SBATCH --cpus-per-task=16

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000

#As the job is not run on the login node where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on the login node before sending the batch job will not help.
module load rspatial-env

#Change to the directory where you have the files
cd $WRKDIR/R_lidar_2019

# Remove and creates new output folder
rm -rf batch_output
mkdir batch_output
srun Rscript --no-save simple_catalog_lidR.R

mv batch_output_$SLURM_JOBID.txt ./batch_output
mv batch_error_$SLURM_JOBID.txt ./batch_output