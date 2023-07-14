#!/bin/bash -l
#SBATCH --account=project_2000599
#SBATCH --output out.txt
#SBATCH --error err.txt

#Partition you want to submit your job to.
#SBATCH -p test

#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:05:00

#Tells the batch job system that this is not a parallel task and only one task should be used. Note that this is one task per job, but array job will actually launch 3 simultaneous jobs.
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load parallel geoconda
#Change to the directory where you have the files

cd /scratch/project_2000599/geocomputing/pdal


find data -name '*.laz' | \
    parallel -I{} -j $SLURM_CPUS_PER_TASK pdal pipeline --readers.las.filename=data/{/.}.laz --writers.gdal.filename=data/{/.}.tif 02_pipeline.json {}