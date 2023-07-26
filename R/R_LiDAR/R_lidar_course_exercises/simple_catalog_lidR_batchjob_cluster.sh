#!/bin/bash -l
# SBATCH --account <YOUR-PROJECT>
#SBATCH --account project_2001659
#Name of the job, this makes it easier to identify your job
#output_%j.txt - Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH --output=batch_output_%j.txt  # File to write the standard output to.
#error_%j.txt - As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH --error=batch_error_%j.txt  # File to write the standard error to.
#Partition you want to submit your job to. 
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#Reserve 5 cores: 1 for master and 4 for workers
#Compared to multicore version, use --ntasks setting, not --cpus-per-task
#SBATCH --ntasks=5  # Number of tasks. Upper limit depends on partition.
#Reserve 10000MB (10GB) of memory per node
#SBATCH --mem=10000  # Real memory required per node.

module load r-env-singularity

# If you have installed packages this helps resolve problems related to those
if test -f ~/.Renviron; then
    sed -i '/TMPDIR/d' ~/.Renviron
    sed -i '/OMP_NUM_THREADS/d' ~/.Renviron   
fi

# Specify a temp folder path
echo "TMPDIR=/scratch/<YOUR-PROJECT>" >> ~/.Renviron

# Remove and creates new output folder
rm -rf batch_output
mkdir batch_output
# Use RMPISNOW instead of Rscript
srun singularity_wrapper exec RMPISNOW --no-save --slave -f simple_catalog_lidR_cluster.R
