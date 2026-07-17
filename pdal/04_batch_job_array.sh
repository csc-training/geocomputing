#!/bin/bash -l
#SBATCH --account=project_200XXXX    # Choose the project to be billed
#SBATCH --partition=small  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --time=00:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --array=1-4  # Indices to specify what array index values should be used. Multiple values may be specified using a comma separated list or a range of values separated by -.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=1000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load python-geo
#Change to the directory where you have the files

cd /scratch/project_2000599/geocomputing/pdal
#Read the file to be processed from a list of input files. This is done by getting the line corresponding to the $SLURM_ARRAY_TASK_ID from the input file list.
input=$(sed -n "$SLURM_ARRAY_TASK_ID"p 04_filelist.csv)

#Create output name from input by exchanging .laz to .tif.
name=$(echo "$input" | cut -f 1 -d '.')
output=data/$(echo "$name" | cut -f 2 -d '/').tif


#Run the pipeline as in previous exercise. Note that it is possible to override input and output files in your pipeline json from the commandline.
pdal pipeline --readers.las.filename=$input --writers.gdal.filename=$output 02_pipeline.json


