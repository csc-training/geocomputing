#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=output.txt  # File to write the standard output to.
#SBATCH --error=errors.txt  # File to write the standard error to.
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.  # Number of tasks. Upper limit depends on partition.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#Equal to number of workers. Max 40 in Puhti.
#SBATCH --cpus-per-task=3  # How many processors work on one task. Upper limit depends on number of CPUs per node.

module load r-env

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
    sed -i '/OMP_NUM_THREADS/d' ~/.Renviron   
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec Rscript --no-save Calc_contours_future_multicore.R
