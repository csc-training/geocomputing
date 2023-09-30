#!/bin/bash
#SBATCH --job-name=GNUparallelTest
#SBATCH --account=project_2007552
#SBATCH --output out.txt
#SBATCH --error err.txt
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test

module load parallel
module load geoconda

datadir=/appl/data/geo/sentinel/s2_example_data/L2A

# For looping through all the files:

# Make a list of input files
readlink -f $datadir/S2* > image_path_list.txt

parallel -a image_path_list.txt python gnu_parallel_example.py