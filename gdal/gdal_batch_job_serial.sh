#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=slurm-%j.out  # File to write the standard output to. %j is replaced by the job ID.
#SBATCH --error=slurm-%j.err  # File to write the standard error to. %j is replaced by the job ID. Defaults to slurm-%j.out if not provided. 
#SBATCH --time 0:05:00
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=300  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

# Load geoconda module to have GDAL commandline tools available.
module load geoconda

# Run the bash script, which includes the GDAL commands.
bash gdal_serial.sh
