#!/bin/bash
# ToDo: change project name in the row below
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=slurm-%j.out  # File to write the standard output to. %j is replaced by the job ID.
#SBATCH --error=slurm-%j.err  # File to write the standard error to. %j is replaced by the job ID. Defaults to slurm-%j.out if not provided. 
#SBATCH --time 0:05:00
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --cpus-per-task=3  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=300  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

# Load geoconda module to have GDAL commandline tools available.
module load parallel geoconda

# Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
# Run the GDAL script for each found file.

find find /appl/data/geo/mml/dem10m/2019/W3/W33 -name '*.tif' | \
    parallel -j $SLURM_CPUS_PER_TASK bash gdal_parallel.sh {}
