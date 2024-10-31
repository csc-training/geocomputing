#!/bin/bash
#SBATCH --account=project_20xxxxx   # Choose the project to be billed
# SBATCH --reservation=geocomputing_thu # Only available during the course
#SBATCH --time=00:10:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=6G            # Memory required per allocated CPU.  Default units are megabytes.
#SBATCH --partition=small            # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# The resources reserved here are only for the master job, so 1 core and moderate memory should be enough.
# The resources for workers are reservd in the Python file.

### Load the geoconda module which has Python and Dask installed
module load geoconda

datadir=/appl/data/geo/sentinel/s2_example_data/L2A

### Run the Dask example. The directory given to the script has 3 Sentinel images
### We also give our project name so the master job is able to launch worker jobs

srun python dask_multinode.py $datadir $SLURM_JOB_ACCOUNT
