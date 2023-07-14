#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output out.txt
#SBATCH --error err.txt
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

module load geoconda
srun python single_core_example.py
