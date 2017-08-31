#!/bin/bash -l
#SBATCH -J python_focal
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 00:00:20
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2
#SBATCH -p serial

# load needed modules
module load geo-env
# move to the directory where the data files locate
cd ~/input_files_folder

python simple_focal_mean.py FILENAME
