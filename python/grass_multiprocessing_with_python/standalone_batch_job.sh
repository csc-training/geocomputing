#!/bin/bash -l
#SBATCH -J python_grass_test
#SBATCH --output=out.txt  # File to write the standard output to.
#SBATCH --error=err.txt  # File to write the standard error to.
#SBATCH -t 00:02:00
#SBATCH --cpus-per-task=5  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=10000  # Real memory required per node.
#SBATCH -p test
module load geo-env fftw grass
python standalone.py 2 2 4
