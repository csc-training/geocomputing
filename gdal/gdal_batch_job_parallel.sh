#!/bin/bash
#SBATCH --account=project_2004306
#SBATCH --job-name gdal_job
#SBATCH --output out.txt
#SBATCH --error err.txt
#SBATCH --time 0:05:00
#SBATCH --partition test
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=300

# Load geoconda module to have GDAL commandline tools available.
module load parallel geoconda

# Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.
# Run the GDAL script for each found file.

find find /appl/data/geo/mml/dem10m/2019/W3/W33 -name '*.tif' | \
    parallel -j $SLURM_CPUS_PER_TASK bash gdal_parallel.sh {}
