#!/bin/bash
#SBATCH --job-name=CNN_excercise
#SBATCH --account=project_2002044
#SBATCH --gres=gpu:v100:1,nvme:1
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:15:00
#SBATCH --partition=gpu

### add reservation

module load solaris

### This uncompresses (unzips) the tar you created from the tiles folder to a local filesystem on the computatation node
tar xf /scratch/project_2002044/students/<YOUR-STUDENT-NUMBER>/spruce_prediction.tar -C $LOCAL_SCRATCH

### Give the local filesystem dir to the python function as argument
srun python 08_2_predict.py $LOCAL_SCRATCH
