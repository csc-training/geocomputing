#!/bin/bash
#SBATCH --account=project_200XXXX   # Choose the project to be billed
# SBATCH --reservation=geocomputing_day2 # Only available during the course
#SBATCH --time=00:10:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=3G            # Memory required per allocated CPU.  Default units are megabytes.
#SBATCH --partition=small            # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# The resources reserved here are only for the master job, so 1 core and moderate memory should be enough.
# The resources for workers are reservd in the Python file.

module load python-geo
srun python dask_multinode.py $SLURM_JOB_ACCOUNT
