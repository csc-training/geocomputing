#!/bin/bash -l
#SBATCH --account <YOUR-PROJECT>
#SBATCH -J basic_rlas
#SBATCH -o out_R.txt
#SBATCH -e err_R.txt
#SBATCH -t 00:15:00
#SBATCH --mem-per-cpu=4000
#SBATCH -p small
#SBATCH -n 1

module load r-env-singularity
srun singularity_wrapper exec Rscript --no-save --slave basic_rlas.R