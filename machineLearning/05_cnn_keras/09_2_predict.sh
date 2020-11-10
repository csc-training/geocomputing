#!/bin/bash
#SBATCH --account=project_2002044
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=0:14:00
#SBATCH --gres=gpu:v100:1
#SBATCH --reservation ml10

module load tensorflow/nvidia-19.11-tf2-py3
srun singularity_wrapper exec python3 09_2_predict.py