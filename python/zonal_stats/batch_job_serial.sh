#!/bin/bash -l
#SBATCH -J python_vrt_mp_test
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 00:00:30
#SBATCH --mem-per-cpu=10
#SBATCH -p serial
#SBATCH -n 1

module load geoconda
srun python /wrk/ekkylli/geocomputing/python/zonal_stats/zonal_stats_serial.py
