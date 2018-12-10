#!/bin/bash -l
#SBATCH -J r_multi_proc
#SBATCH -o output_%j.txt
#SBATCH -e errors_%j.txt
#SBATCH -t 00:04:00
#SBATCH --ntasks=3
#Test partition is for small test jobs only. For real jobs use either serial or parallel partition dependeing on how many nodes you need
#SBATCH -p test
#SBATCH --mem-per-cpu=1000

module load rspatial-env
srun RMPISNOW --no-save -f Calc_contours_snow.R
