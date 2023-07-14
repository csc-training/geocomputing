#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=01:00:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G

module load force
srun force-level2 /users/johannes/force/LEVEL2_parameters.prm
