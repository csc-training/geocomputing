#!/bin/bash
#SBATCH --account=project_200xxxx    # Choose the project to be billed
#SBATCH --output=slurm-%j.out  # File to write the standard output to. %j is replaced by the job ID.
#SBATCH --error=slurm-%j.err  # File to write the standard error to. %j is replaced by the job ID. Defaults to slurm-%j.out if not provided. 
#SBATCH --time=0:05:00  # Maximum duration of the job. Upper limit depends on partition.
#SBATCH --partition=test  # Which queue to use. Defines maximum time, memory, tasks, nodes and local storage for job
#SBATCH --nodes=1  # Number of compute nodes. Upper limit depends on partition.
#SBATCH --ntasks=1  # Number of tasks. Upper limit depends on partition.
#SBATCH --mem-per-cpu=4000  # Minimum memory required per usable allocated CPU.  Default units are megabytes.

#module load grassgis
module load qgis

GRASS_DIR=/scratch/project_2000599/grass
GRASS_DB_DIR=$GRASS_DIR/db
GRASS_LOCATION_DIR=$GRASS_DB_DIR/3067

# create a directory to hold the location used for processing
mkdir -p $GRASS_DB_DIR/db

# create new temporary location for the job, exit after creation of this location
grass -c epsg:3067 $GRASS_LOCATION_DIR -e

# now use this new location and run the job
grass --exec python3 python_scripting_serial.py 

# Optional, delete temporary location 
#rm -rf $GRASS_LOCATION_DIR
