#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=out_R.txt  # File to write the standard output to.
#SBATCH --error=err_R.txt  # File to write the standard error to.
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --mem-per-cpu=4000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.

module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
fi


srun singularity_wrapper exec Rscript --no-save --slave basic_rlas.R
