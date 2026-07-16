#!/bin/bash -l
#SBATCH --account project_200XXXX
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=5  # How many processors work on one task. Upper limit depends on number of CPUs per node.

#Tells the batch job sytem to reserve 8000MB (8GB) of memory for core
#SBATCH --mem-per-cpu=8000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

module load r-env

# Match thread number with set_lidr_threads(n) setting in the R-script
# echo "OMP_NUM_THREADS=2" >> ~/.Renviron

# Remove and creates new output folder
rm -rf batch_output_multicore
mkdir batch_output_multicore

srun Rscript --no-save simple_catalog_lidR_multicore.R
