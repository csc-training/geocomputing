#!/bin/bash
#SBATCH --job-name=fullyConnectedRegressor
#SBATCH --account=<add-project-here>
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00
#SBATCH --partition=gpu

module load tensorflow/2.0.0

srun python deepRegression.py