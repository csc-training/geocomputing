#!/bin/bash
#SBATCH --account=project_2001659
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4000

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
grass --exec python3 pygrass_serial.py 

# Optional, delete temporary location 
rm -rf $GRASS_LOCATION_DIR
