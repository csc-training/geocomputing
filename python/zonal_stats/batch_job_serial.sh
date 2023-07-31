#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.

module load geoconda
srun python zonal_stats_serial.py
