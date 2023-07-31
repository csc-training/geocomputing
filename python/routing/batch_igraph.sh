#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH --output=out_%J.txt  # File to write the standard output to.
#SBATCH --error=err_%J.txt  # File to write the standard error to.
#SBATCH --time=00:15:00  # Maximum duration of the job. Upper limit depends on partition.
#Number of reserved cores, this number can be later accessed with $SLURM_CPUS_PER_TASK
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#We're operating with shared memory so reserve total amount of memory, not per cpu
#SBATCH --mem=12000  # Real memory required per node.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

# load needed modules
module load geoconda

#Pass number of cores reserved to python script as argument, so that correct number of processes can be started
python igraph_parallel.py $SLURM_CPUS_PER_TASK
