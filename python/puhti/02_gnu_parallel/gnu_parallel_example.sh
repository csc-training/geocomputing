#!/bin/bash
#SBATCH --account=project_20xxxxx   # Choose the project to be billed
# SBATCH --reservation=geocomputing_thu # Only available during the course
#SBATCH --time=00:05:00             # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1                  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=3           # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=2G            # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small            # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load parallel
module load geoconda

datadir=/appl/data/geo/sentinel/s2_example_data/L2A

# For looping through all the files:

# Make a list of input files
readlink -f $datadir/S2* > image_path_list.txt

parallel -a image_path_list.txt python gnu_parallel_example.py
