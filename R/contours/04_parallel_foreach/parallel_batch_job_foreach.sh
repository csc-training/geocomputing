#!/bin/bash -l
#SBATCH --account=<YOUR-PROJECT>
#SBATCH -J r_multi_proc
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH -t 00:05:00
#SBATCH --ntasks=3
#Test partition is used for testing, for real jobs use either serial or parallel depending on how many nodes you need.
#SBATCH -p test
#SBATCH --mem-per-cpu=1000

module load r-env-singularity
srun singularity_wrapper exec Rscript --no-save --slave Calc_contours_foreach.R
