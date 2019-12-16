#!/bin/bash
#SBATCH --job-name=dask_test
#SBATCH --account=<YOUR-PROJECT>
#SBATCH --time=00:15:00
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=test

module load geoconda

srun python ndvi_dask_example.py
