#!/bin/bash
#SBATCH --job-name=MultiprocessingTest
#SBATCH --account=project_2000745
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test

module load geoconda
srun python multiprocessing_example.py 
