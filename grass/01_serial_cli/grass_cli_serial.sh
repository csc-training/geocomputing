#!/bin/bash
#SBATCH --account=project_2001659
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH -t 0:05:00
#SBATCH -p test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4000

module load qgis

GRASS_DIR=/scratch/project_2000599/grass
GRASS_DB_DIR=$GRASS_DIR/db
GRASS_LOCATION_DIR=$GRASS_DB_DIR/3067
MAPSET_DIR=$GRASS_LOCATION_DIR/PERMANENT/
SCRIPTS_DIR=/scratch/project_2000599/geocomputing/grass/01_serial_cli

# create a directory to hold the location used for processing
mkdir -p $GRASS_DB_DIR/db

# create new temporary location for the job, exit after creation of this location
grass -c epsg:3067 $GRASS_LOCATION_DIR -e

# define job file as environmental variable
# Make sure first that job file has executing rights, use chmod command for fixing
export GRASS_BATCH_JOB=$SCRIPTS_DIR/grass_cli.sh

# now we can use this new location and run the job defined via GRASS_BATCH_JOB
grass $MAPSET_DIR

#### 3) CLEANUP
# switch back to interactive mode, for the next GRASS GIS session
unset GRASS_BATCH_JOB

# delete temporary location 
rm -rf $GRASS_LOCATION_DIR
