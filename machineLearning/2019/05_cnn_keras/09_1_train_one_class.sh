#!/bin/bash
#SBATCH --account=project_2002044
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=6G
#SBATCH --time=6:00:00
#SBATCH --gres=gpu:v100:1,nvme:1 #Local disk in Gb

module load tensorflow/2.0.0
#tar cvf spruce.tar image_training_tiles_650 label_tiles_650
tar xf /scratch/project_2002044/test/johannes/tiles/spruce.tar -C $LOCAL_SCRATCH

ls $LOCAL_SCRATCH

srun python3 train.py $LOCAL_SCRATCH
