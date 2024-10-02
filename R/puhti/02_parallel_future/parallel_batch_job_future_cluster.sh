#!/bin/bash -l
#SBATCH --account=project_20xxxxx    # Choose the project to be billed
#SBATCH --output=output.txt  # File to write the standard output to.
#SBATCH --error=errors.txt  # File to write the standard error to.
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#Reserve cores for 1 master + 3 workers
#SBATCH --ntasks=4  # Number of tasks. Upper limit depends on partition.
#Test partition is used for testing, for real jobs use either serial or parallel depending on how many nodes you need.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load r-env

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
    sed -i '/OMP_NUM_THREADS/d' ~/.Renviron   
fi

# Specify a temp folder path
# echo "TMPDIR=/scratch/<project>/tmp" >> ~/.Renviron
echo "TMPDIR=$PWD/tmp" >> ~/.Renviron

srun apptainer_wrapper exec RMPISNOW --no-save --slave -f Calc_contours_future_cluster.R
