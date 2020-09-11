#!/bin/bash
#SBATCH --job-name=classificationExcercise
#SBATCH --account=project_2002044
#SBATCH --time=00:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2G
#SBATCH --partition=small

module load geoconda

srun python 05_classification.py
