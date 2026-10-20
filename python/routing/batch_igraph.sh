#!/bin/bash -l
#SBATCH -A project_200XXXX
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=12000  # Real memory required per node.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# load needed modules
module load python-geo

#Pass number of cores reserved to python script as argument, so that correct number of processes can be started
python igraph_parallel.py $SLURM_CPUS_PER_TASK
