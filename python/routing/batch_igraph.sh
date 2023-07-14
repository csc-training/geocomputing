#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH -J python_igraph
#SBATCH --output out_%J.txt
#SBATCH --error err_%J.txt
#SBATCH -t 00:15:00
#Number of reserved cores, this number can be later accessed with $SLURM_CPUS_PER_TASK
#SBATCH --cpus-per-task=4
#We're operating with shared memory so reserve total amount of memory, not per cpu
#SBATCH --mem=12000
#SBATCH -p test

# load needed modules
module load geoconda

#Pass number of cores reserved to python script as argument, so that correct number of processes can be started
python igraph_parallel.py $SLURM_CPUS_PER_TASK
