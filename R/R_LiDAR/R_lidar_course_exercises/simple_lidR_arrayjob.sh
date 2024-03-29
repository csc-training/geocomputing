#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#Name of the job, this makes it easier to identify your job
#output_%j.txt - Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH --output=array_output/array_output_%j.txt  # File to write the standard output to.
#error_%j.txt - As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH --error=array_output/array_error_%j.txt  # File to write the standard error to.
#Partition you want to submit your job to. Possible values are serial, parallel, longrun, hugemem and test. In this excerecise we use test as it is for testing, but it shouldn't be used for serious work. See <link> for details.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#--array - Tells the batch job system that this is an array job that should be run 3 times. It creates a variable named $SLURM_ARRAY_TASK_ID which will get a different value ranging from 1 to 3 for each task.
#SBATCH --array=1-6  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#Tells the batch job system that this is not a parallel task and only one task should be used. Note that this is one task per job, but array job will actually launch 3 simultaneous jobs.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#As the job is not run on the login node where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on the login node before sending the batch job will not help.
module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

#Read the file to be processed from a list of input files. This is done by getting the line corresponding to the $SLURM_ARRAY_TASK_ID from the input file list.
input=$(sed -n "$SLURM_ARRAY_TASK_ID"p las_files.txt)

srun singularity_wrapper exec Rscript --no-save simple_lidR.R $input
