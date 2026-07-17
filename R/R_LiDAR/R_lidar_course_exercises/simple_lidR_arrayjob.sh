#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --array=1-6  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#As the job is not run on the login node where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on the login node before sending the batch job will not help.
module load r-env

#Read the file to be processed from a list of input files. This is done by getting the line corresponding to the $SLURM_ARRAY_TASK_ID from the input file list.
input=$(sed -n "$SLURM_ARRAY_TASK_ID"p las_files.txt)

srun Rscript --no-save simple_lidR.R $input
