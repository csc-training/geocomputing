#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=4G  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

### Load the geoconda module which has Python and Dask installed
module load geoconda

### Run the Dask example. The directory given to the script hosts 3 Sentinel images
### We also give our project name so the master job is able to launch worker jobs
srun python dask_multinode.py /appl/data/geo/sentinel/s2_example_data/L2A project_2001659