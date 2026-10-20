#!/bin/bash
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=4G  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load python-geo
srun python 03_python_pipeline_multiprocessing.py
