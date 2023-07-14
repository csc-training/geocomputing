#!/bin/bash
#SBATCH --account=<YOUR-PROJECT>
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G

module load force
srun force-level2 /users/johannes/force/LEVEL2_parameters.prm
