#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --partition=gpu  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=5  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=6G  # Real memory required per node.
#SBATCH --time=1:00:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --gres=gpu:v100:1,nvme:1 # How many and which GPU to use for the job. And how much local disk to reserve. Default units for nvme is gigabytes. 

module load tensorflow/nvidia-19.11-tf2-py3
#tar cvf spruce.tar image_training_tiles_650 label_tiles_650
#TOFIX: set your own tiles folder
tar xf /scratch/project_2002044/test/student_0000/tiles/spruce.tar -C $LOCAL_SCRATCH

echo $LOCAL_SCRATCH
ls $LOCAL_SCRATCH

srun singularity_wrapper exec python3 09_1_train.py $LOCAL_SCRATCH
