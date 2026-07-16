#!/bin/bash
#SBATCH --account=project_200XXXX    # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=00:02:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --array=1-3  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load r-env

# Select the inputfile from row n to the array job n.
file_path=$(sed -n ${SLURM_ARRAY_TASK_ID}p ../mapsheets_URLs.txt)

srun Rscript Contours_array.R $name
