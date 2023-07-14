#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH -J r_multi_proc
#SBATCH --output output.txt
#SBATCH --error errors.txt
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

