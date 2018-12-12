#!/bin/bash -l
#SBATCH -J python_igraph
#SBATCH -o out_%J.txt
#SBATCH -e err_%J.txt
#SBATCH -t 00:10:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=6000
#SBATCH -p test

# load needed modules
module load geoconda
# move to the directory where the example was downloaded
cd $WRKDIR/geocomputing/python/routing
python nx_parallel.py $SLURM_CPUS_PER_TASK
