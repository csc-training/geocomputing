#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#Equal to number of workers. Max 386 in Roihu.
#SBATCH --cpus-per-task=3  # How many processors work on one task. Upper limit depends on number of CPUs per node.

module load r-env
srun Rscript --no-save Calc_contours_future_multicore.R