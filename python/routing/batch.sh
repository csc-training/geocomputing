#!/bin/bash -l
#SBATCH -J python_igraph
#SBATCH -o out_%J.txt
#SBATCH -e err_%J.txt
#SBATCH -t 00:15:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=12000
#SBATCH -p test

# load needed modules
module load geoconda
# move to the directory where the example was downloaded
cd $WRKDIR/graph_parallel
python igraph_parallel.py $SLURM_CPUS_PER_TASK
