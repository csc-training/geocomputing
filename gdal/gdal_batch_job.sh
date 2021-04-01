#!/bin/bash
#SBATCH --account=project_2002044
#SBATCH -J rspatial_job
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=300

module load gcc/9.1.0 gdal

srun ./gdal.sh