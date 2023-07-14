#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=out.txt  # File to write the standard output to.
#SBATCH --error=err.txt  # File to write the standard error to.
#SBATCH --time 0:05:00
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=300  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

# Load geoconda module to have GDAL commandline tools available.
module load geoconda

# Run the bash script, which includes the GDAL commands.
bash gdal_serial.sh
