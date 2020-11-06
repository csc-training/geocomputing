#!/bin/bash
#SBATCH --job-name=deepRegression
#SBATCH --account=project_2002044
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00
#SBATCH --partition=gputest
#SBATCH --gres=gpu:v100:1

# Add these later
# --reservation ml_training
# --partition=gpu

module load tensorflow/2.0.0

srun python 06_deepRegression.py
