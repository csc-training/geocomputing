#!/bin/bash
#SBATCH --account=project_2001659
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test

module load geoconda
srun python 07_pdal_ground.py