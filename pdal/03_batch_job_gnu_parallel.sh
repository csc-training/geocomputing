#!/bin/bash -l
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=slurm-%j.out  # File to write the standard output to. %j is replaced by the job ID.
#SBATCH --error=slurm-%j.err  # File to write the standard error to. %j is replaced by the job ID. Defaults to slurm-%j.out if not provided. 

#Partition you want to submit your job to.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job

#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.

#Tells the batch job system that this is not a parallel task and only one task should be used. Note that this is one task per job, but array job will actually launch 3 simultaneous jobs.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --cpus-per-task=4  # How many processors work on one task. Upper limit depends on number of CPUs per node.

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load parallel geoconda
#Change to the directory where you have the files

cd /scratch/project_2000599/geocomputing/pdal


find data -name '*.laz' | \
    parallel -I{} -j $SLURM_CPUS_PER_TASK pdal pipeline --readers.las.filename=data/{/.}.laz --writers.gdal.filename=data/{/.}.tif 02_pipeline.json {}