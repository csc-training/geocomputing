#!/bin/bash
#SBATCH --job-name=CNN_excercise
#SBATCH --account=project_2002044
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:15:00
#SBATCH --partition=gpu
#SBATCH --reservation ml_training

module load solaris

srun python 08_classificationCNN.py