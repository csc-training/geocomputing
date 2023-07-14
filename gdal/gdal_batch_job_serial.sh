#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output out.txt
#SBATCH --error err.txt
#SBATCH --time 0:05:00
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=300

# Load geoconda module to have GDAL commandline tools available.
module load geoconda

# Run the bash script, which includes the GDAL commands.
bash gdal_serial.sh
