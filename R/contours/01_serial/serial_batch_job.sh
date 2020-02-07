#!/bin/bash
#SBATCH --account=<YOUR-PROJECT>
#SBATCH -J rspatial_job
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000

module load r-env
srun Rscript --no-save Contours_simple.R
