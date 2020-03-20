#!/bin/bash
#SBATCH --job-name=deepClassification
#SBATCH --account=project_2002044
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:14:00
#SBATCH --partition=gputest
#SBATCH --reservation ml_training

module load tensorflow/2.0.0

srun python 07_deepClassification.py
