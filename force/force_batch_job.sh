#!/bin/bash
#SBATCH --job-name=force_batch
#SBATCH --account=<YOUR-PROJECT>
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G

module load force
singularity_wrapper exec force-level2 /users/johannes/force/LEVEL2_parameters.prm