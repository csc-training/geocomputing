#!/bin/bash
#SBATCH --job-name=deepClassification
#SBATCH --account=project_2002044
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:14:00
#SBATCH --partition=gputest


# Add these later
# --reservation ml_training
# --gres=gpu:v100:1
# --partition=gpu

module load tensorflow/nvidia-20.03-tf2-py3

srun singularity_wrapper exec python 07_deepClassification.py
