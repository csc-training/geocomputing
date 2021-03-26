#!/bin/bash
#SBATCH --job-name=DaskMulticore
#SBATCH --account=<project>
#SBATCH --time=00:05:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test

### Load the geoconda module which has Python and Dask installed
module load geoconda

### Run the Dask example. The directory given to the script hosts 3 Sentinel images
srun python dask_multicore.py /appl/data/geo/sentinel/s2_example_data/L2A