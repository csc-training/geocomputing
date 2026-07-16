#!/bin/bash
#SBATCH --account=project_2000599    # Choose the project to be billed
#SBATCH --time=00:20:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=10  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=10G  # Minimum memory required per allocated CPU.  Default units are megabytes.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# Load the python-geo module which has Python with Dask, Xarray and STAC libraries
module load python-geo

# Run the Python code. 
python csc_stac_example.py
