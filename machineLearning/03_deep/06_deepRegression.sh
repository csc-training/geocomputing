#!/bin/bash
#SBATCH --job-name=deepRegression
#SBATCH --account=project_2002044
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --reservation=ml_training_10

module load tensorflow/nvidia-19.11-tf2-py3

srun python 06_deepRegression.py
