#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --mem-per-cpu=4000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.

module load r-env
srun Rscript --no-save basic_rlas.R
