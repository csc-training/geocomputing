#!/bin/bash -l
#SBATCH --account project_200XXXX
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#Reserve 5 cores: 1 for master and 4 for workers
#Compared to multicore version, use --ntasks setting, not --cpus-per-task
#SBATCH --ntasks=5  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem=10000  # Real memory required per node.

module load r-env

# Remove and creates new output folder
rm -rf batch_output
mkdir batch_output

# Use RMPISNOW instead of Rscript
srun RMPISNOW --no-save --slave -f simple_catalog_lidR_cluster.R
