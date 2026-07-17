#!/bin/bash
# ToDo: change project name in the row below
#SBATCH --account=project_200XXXX  # Choose the project to be billed
# SBATCH --reservation=geocomputing_day1 # Only available during the course
#SBATCH --time 0:05:00
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=300  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

# Load python-geo module to have GDAL commandline tools available.
module load python-geo

# Run the bash script, which includes the GDAL commands.
srun bash gdal_serial.sh
