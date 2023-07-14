#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=gpu  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=1  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=4G  # Real memory required per node.
#SBATCH --time=0:14:00  # Maximum duration of the job. Upper limit depends on partition.  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --gres=gpu:v100:1  # How many and which GPU to use for the job. 

module load tensorflow/nvidia-19.11-tf2-py3
srun singularity_wrapper exec python3 09_2_predict.py
