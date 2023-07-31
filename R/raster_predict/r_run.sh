#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=output.txt  # File to write the standard output to.
#SBATCH --error=errors.txt  # File to write the standard error to.
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=4  # Number of tasks. Upper limit depends on partition.
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --mem=1000  # Real memory required per node.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load r-env-singularity

if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi

srun singularity_wrapper exec RMPISNOW --no-save -f rtest.R

