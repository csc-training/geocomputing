#!/bin/bash
#SBATCH --account=project_2004306
#SBATCH -J gdal_job
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=300

module load parallel geoconda

#Find the files that have .tif ending, we do not want to process the .tif.aux.xml files in the same folders.

find find /appl/data/geo/mml/dem10m/2019/W3/W33 -name '*.tif' | \
    parallel -j $SLURM_CPUS_PER_TASK bash gdal_parallel.sh {}
