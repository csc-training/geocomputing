#!/bin/bash -l
#SBATCH -J python_igraph
#SBATCH -o out_%J.txt
#SBATCH -e err_%J.txt
#SBATCH -t 00:10:00
#Number of resrved cores, this number can be later accessed with $SLURM_CPUS_PER_TASK
#SBATCH --cpus-per-task=4
#We're operating with shared memory so reserve total amount of memory, not per cpu
#SBATCH --mem=6000
#SBATCH -p test

# load needed modules
module load geoconda
# move to the directory where the example was downloaded
cd $WRKDIR/geocomputing/python/routing
#Pass number of cores reserved to python script as argument, so that correct number of processes can be started
python nx_parallel.py $SLURM_CPUS_PER_TASK
