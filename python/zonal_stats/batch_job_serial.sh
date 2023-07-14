#!/bin/bash -l
#SBATCH -A <YOUR-PROJECT-HERE>
#SBATCH -J python_vrt_mp_test
#SBATCH -t 00:10:00
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.
#SBATCH -p test
#SBATCH -n 1

module load geoconda
srun python zonal_stats_serial.py
