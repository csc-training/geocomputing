#!/bin/bash
#SBATCH --job-name=DaskMultinode
#SBATCH --account=project_2001659
#SBATCH --time=00:15:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --partition=test

### Load the geoconda module which has Python and Dask installed
module load geoconda

### Run the Dask example. The directory given to the script hosts 3 Sentinel images
### We also give our project name so the master job is able to launch worker jobs
srun python dask_multinode.py /appl/data/geo/sentinel/s2_example_data/L2A project_2001659