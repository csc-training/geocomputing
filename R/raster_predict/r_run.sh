#!/bin/bash -l
#SBATCH --account=<YOUR-PROJECT>
#SBATCH -J r_multi_proc
#SBATCH -o output.txt
#SBATCH -e errors.txt
#SBATCH -t 00:10:00
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --mem=1000
#SBATCH -p small

module load r-env-singularity

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

srun singularity_wrapper exec RMPISNOW --no-save -f rtest.R

