#!/bin/bash
#SBATCH --job-name=deepRegression
#SBATCH --account=project_2002044
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00
#SBATCH --partition=gpu
#SBATCH --reservation ml_training

module load tensorflow/2.0.0

srun python 06_deepRegression.py