#!/bin/bash -l
#SBATCH -J python_grass_test
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 00:02:00
#SBATCH --cpus-per-task=5
#SBATCH --mem=1000
#SBATCH -p parallel
module load geo-env fftw grass
grass72 --exec python within_grass.py 2 2 4
