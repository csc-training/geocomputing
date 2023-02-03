#!/bin/bash
#SBATCH --account=project_2004306
#SBATCH --job-name gdal_job
#SBATCH --output out.txt
#SBATCH --error err.txt
#SBATCH --time 0:05:00
#SBATCH --partition test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=300

# Load geoconda module to have GDAL commandline tools available.
module load geoconda

# Run the bash script, which includes the GDAL commands.
bash gdal_serial.sh
