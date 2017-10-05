#!/bin/bash -l
#SBATCH -J r_multi_proc
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH -t 00:01:00
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --mem=1000

module load rspatial-env
srun RMPISNOW --no-save -f rtest.R

