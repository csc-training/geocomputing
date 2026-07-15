#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#Reserve cores for 1 master + 3 workers
#SBATCH --ntasks=4  # Number of tasks. Upper limit depends on partition.
#Test partition is used for testing, for real jobs use either serial or parallel depending on how many nodes you need.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load r-env
srun RMPISNOW --no-save --slave -f Calc_contours_future_cluster.R
