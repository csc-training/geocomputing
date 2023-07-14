#!/bin/bash -l
#SBATCH --output=out.txt  # File to write the standard output to.
#SBATCH --error=err.txt  # File to write the standard error to.
#SBATCH --time=00:02:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --cpus-per-task=5  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=1000  # Real memory required per node.
#SBATCH --partition=parallel  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
module load geo-env fftw grass
grass72 --exec python within_grass.py 2 2 4
