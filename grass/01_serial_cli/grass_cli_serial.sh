#!/bin/bash
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --time=0:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=4000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load grassgis

# Run the GRASS script with temporary location
grass --tmp-location EPSG:3067 --exec bash grass_cli.sh
