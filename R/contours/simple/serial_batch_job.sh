#!/bin/bash
#SBATCH -J rspatial_job
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000
#
module load rspatial-env
srun Rscript --no-save Contours_simple.R
