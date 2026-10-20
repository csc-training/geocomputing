#!/bin/bash
#SBATCH --account=project_200XXXX    # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=0:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load r-env
srun Rscript --no-save Contours_simple.R