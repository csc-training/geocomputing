#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=1000  # Real memory required per node.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load geoconda
python zonal_stats_parallel.py
