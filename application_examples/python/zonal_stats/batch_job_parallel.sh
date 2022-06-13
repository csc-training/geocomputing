#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH -J python_vrt_mp_test
#SBATCH -t 00:05:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=1000
#SBATCH -p small

module load geoconda
python zonal_stats_parallel.py
