#!/bin/bash -l
#SBATCH -J basic_rlas
#SBATCH -o out_R.txt
#SBATCH -e err_R.txt
#SBATCH -t 00:15:00
#SBATCH --mem-per-cpu=15000
#SBATCH -p serial
#SBATCH -n 1

module load rspatial-env
srun Rscript --no-save --slave basic_rlas.R


used_slurm_resources.bash

# See if your script is running with:
# squeue -l -u $USER
