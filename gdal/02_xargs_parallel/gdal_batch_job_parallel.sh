#!/bin/bash
# ToDo: change project name in the row below
#SBATCH --account=project_200XXXX  # Choose the project to be billed
# SBATCH --reservation=geocomputing_day1 # Only available during the course
#SBATCH --time 0:05:00
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=300  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

# Load python-geo module to have GDAL commandline tools available.
module load python-geo

# Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
# Run the GDAL script for each of the found files.

find /dataset/project_2019680/mml/dem10m/2019/W3/W33 -name '*.tif' -print0 | \
    xargs -0 -n1 -P $SLURM_CPUS_PER_TASK bash gdal_parallel.sh

# -0 helps to read in the file names from find properly
# -P defines how many processes in parallel
