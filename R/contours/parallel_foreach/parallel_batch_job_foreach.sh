#!/bin/bash -l
#SBATCH -J r_multi_proc
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH -t 00:01:00
#SBATCH --ntasks=3
#SBATCH -p test
#SBATCH --mem-per-cpu=1000

module load rspatial-env
srun Rscript --no-save --slave Calc_contours_foreach.R
