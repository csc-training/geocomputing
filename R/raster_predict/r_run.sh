#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH -J r_multi_proc
#SBATCH --output=output.txt  # File to write the standard output to.
#SBATCH --error=errors.txt  # File to write the standard error to.
#SBATCH -t 00:10:00
#SBATCH --ntasks=4  # Number of tasks. Upper limit depends on partition.
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --mem=1000  # Real memory required per node.
#SBATCH -p small

module load r-env-singularity

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

srun singularity_wrapper exec RMPISNOW --no-save -f rtest.R

