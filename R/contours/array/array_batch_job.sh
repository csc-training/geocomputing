#!/bin/bash
#SBATCH -J array_job
#SBATCH -o array_job_out_%j.txt
#SBATCH -e array_job_err_%j.txt
#SBATCH -t 00:02:00
#SBATCH --mem-per-cpu=4000
#SBATCH --array=1-3
#SBATCH -n 1
#SBATCH -p serial

module load rspatial-env
# move to the directory where the data files locate
cd ~/R_spatial_2017
# set input file to be processed
name=$(sed -n "$SLURM_ARRAY_TASK_ID"p mapsheets.txt)
# run the analysis command
srun Rscript ~/R_spatial_2017/Calc_contours.R $name
