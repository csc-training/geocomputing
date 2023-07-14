#!/bin/bash -l
#SBATCH --account <YOUR-PROJECT>
#SBATCH -J basic_rlas
#SBATCH --output out_R.txt
#SBATCH --error err_R.txt
#SBATCH -t 00:15:00
#SBATCH --mem-per-cpu=4000
#SBATCH -p small
#SBATCH -n 1

module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi


srun singularity_wrapper exec Rscript --no-save --slave basic_rlas.R
