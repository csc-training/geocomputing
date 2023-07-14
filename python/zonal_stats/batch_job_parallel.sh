#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH -J python_vrt_mp_test
#SBATCH -t 00:05:00
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem=1000  # Real memory required per node.
#SBATCH -p small

module load geoconda
python zonal_stats_parallel.py
