#!/bin/bash
#SBATCH --account=project_2002044
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=6G
#SBATCH --time=2:00:00
#SBATCH --gres=gpu:v100:1,nvme:1 #Local disk in Gb

module load tensorflow/2.0.0
#tar cvf forest.tar image_training_tiles_650 labels_all_classes_tiles_650
#TOFIX: set your own tiles folder
tar xf /scratch/project_2002044/test/student_0000/tiles/forest.tar -C $LOCAL_SCRATCH

echo $LOCAL_SCRATCH
ls $LOCAL_SCRATCH

srun python3 09_1_train.py $LOCAL_SCRATCH
