#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --partition=gpu  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --gres=gpu:v100:1

module load tensorflow/nvidia-19.11-tf2-py3
srun singularity_wrapper exec python 06_deepRegression.py
