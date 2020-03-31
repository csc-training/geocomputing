#!/bin/bash
#SBATCH --job-name=ArrayJobTest
#SBATCH --output=array_job_out_%A_%a.txt
#SBATCH --error=array_job_err_%A_%a.txt
#SBATCH --account=<project>
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3G
#SBATCH --partition=small
#SBATCH --array=1-3

module load geoconda

image_path_list=${readlink -f <INSERT_PATH_TO_SENTINEL_FOLDERS>/*}
image=$(sed -n ${SLURM_ARRAY_TASK_ID}p image_path_list)

srun python array_job_example.py ${image}