#!/bin/bash
#SBATCH --job-name=MultiprocessingTest
#SBATCH --account=<project>
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=3G
#SBATCH --partition=test

module load geoconda
srun python multiprocessing_example.py