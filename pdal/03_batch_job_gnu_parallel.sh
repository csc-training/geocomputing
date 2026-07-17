#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load parallel python-geo
#Change to the directory where you have the files

cd /scratch/project_2000599/geocomputing/pdal


find data -name '*.laz' | \
    parallel -I{} -j $SLURM_CPUS_PER_TASK pdal pipeline --readers.las.filename=data/{/.}.laz --writers.gdal.filename=data/{/.}.tif 02_pipeline.json {}