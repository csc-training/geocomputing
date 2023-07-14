#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH -J python_igraph
#SBATCH --output=out_%J.txt  # File to write the standard output to.
#SBATCH --error=err_%J.txt  # File to write the standard error to.
#SBATCH -t 00:10:00
#Number of reserved cores, this number can be later accessed with $SLURM_CPUS_PER_TASK
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#We're operating with shared memory so reserve total amount of memory, not per cpu
#SBATCH --mem=6000  # Real memory required per node.
#SBATCH -p test

# load needed modules
module load geoconda
#Pass number of cores reserved to python script as argument, so that correct number of processes can be started
python nx_parallel.py $SLURM_CPUS_PER_TASK
