#!/bin/bash 
#SBATCH --job-name=deepClassifier
#SBATCH --account=project_2001659
#SBATCH --output=output_%j.txt
#SBATCH --error=errors_%j.txt
#SBATCH --time=01:00:00
#SBATCH --nodes 1
#SBATCH --partition=small
#SBATCH --mail-type=END
#SBATCH --mail-user=ziya.yektay@csc.fi
#SBATCH --mem-per-cpu=15000
#SBATCH --cpus-per-task=4

module load geoconda/3.7

srun python deepClassification.py
