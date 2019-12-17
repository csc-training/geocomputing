#!/bin/bash
#SBATCH --account=project_2000599
#SBATCH -J array_job
#SBATCH -o array_job_out_%A_%a.txt
#SBATCH -e array_job_err_%A_%a.txt
#SBATCH -t 00:02:00
#SBATCH --mem-per-cpu=4000
#SBATCH --array=1-3
#SBATCH -n 1
#SBATCH -p serial

module load r-env
# move to the directory where the data files locate
cd ~/git/geocomputing/R/contours/array
# set input file to be processed
name=$(sed -n "$SLURM_ARRAY_TASK_ID"p ../mapsheets.txt)
# run the analysis command
srun Rscript Calc_contours.R $name
