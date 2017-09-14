#!/bin/bash -l
#SBATCH -J r_multi_proc
#SBATCH -o output_%j.txt
#SBATCH -e errors_%j.txt
#SBATCH -t 00:04:00
#SBATCH --ntasks=3
#SBATCH -p parallel
#SBATCH --mem-per-cpu=1000

module load rspatial-env
srun RMPISNOW --no-save -f Calc_contours_snow.R
