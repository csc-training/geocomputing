#!/bin/bash
#SBATCH -A project_2000599
#SBATCH -c 10
#SBATCH -p gputest
#SBATCH --gres=gpu:v100:1
#SBATCH -t 0:30:00
#SBATCH --mem=64G

module load solaris
srun python CNNPredictSpruceAreas.py