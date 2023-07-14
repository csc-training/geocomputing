#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

### Load the geoconda module which has Python and Dask installed
module load geoconda

### Run the Dask example. The directory given to the script hosts 3 Sentinel images
srun python dask_singlenode.py /appl/data/geo/sentinel/s2_example_data/L2A